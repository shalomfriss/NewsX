"""Middle East analysis agent for producing structured article assessments."""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import textwrap
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Protocol

from src.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Base exception for agent-related failures."""


class LLMGenerationError(AgentError):
    """Raised when the language model cannot generate a response."""


class LLMClient(Protocol):
    """Protocol describing the language model interface."""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate text from the underlying language model."""


@dataclass
class MiddleEastAnalysisConfig:
    """Runtime configuration for the Middle East analysis agent."""

    input_dir: Path = Path("news_md")
    output_dir: Path = Path("news_analysis_md")
    model: str = "gpt-4o-mini"
    temperature: float = 0.1
    max_retries: int = 3
    retry_delay_seconds: float = 5.0
    limit: Optional[int] = None
    dry_run: bool = False


class OpenAILLMClient:
    """Thin wrapper around the OpenAI Responses or Chat Completions API."""

    def __init__(self, model: str, temperature: float, api_key: Optional[str] = None):
        self.model = model
        self.temperature = temperature
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise AgentError(
                "OPENAI_API_KEY must be set in the environment for the analysis agent"
            )

        try:
            from openai import OpenAI

            self._client = OpenAI(api_key=api_key)
            self._use_responses_api = True
            self._client_module = None
        except ImportError:
            try:
                import openai
            except ImportError as exc:
                raise AgentError(
                    "The 'openai' package is required to run the analysis agent"
                ) from exc

            openai.api_key = api_key
            self._client = None
            self._client_module = openai
            self._use_responses_api = False

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate text with retries handled by the caller."""
        if self._use_responses_api:
            return self._generate_with_responses(system_prompt, user_prompt)
        return self._generate_with_chat(system_prompt, user_prompt)

    def _generate_with_responses(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self._client.responses.create(
                model=self.model,
                temperature=self.temperature,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
            )
        except Exception as exc:  # pragma: no cover - upstream library exception
            raise LLMGenerationError("OpenAI Responses API call failed") from exc

        response_data = response.model_dump()
        output_items = response_data.get("output", [])
        fragments: List[str] = []
        for item in output_items:
            for block in item.get("content", []):
                if block.get("type") == "output_text":
                    fragments.append(block.get("text", ""))
        if not fragments:
            raise LLMGenerationError("No text returned from OpenAI Responses API")
        return "".join(fragments).strip()

    def _generate_with_chat(self, system_prompt: str, user_prompt: str) -> str:
        try:
            completion = self._client_module.ChatCompletion.create(
                model=self.model,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
            )
        except Exception as exc:  # pragma: no cover - upstream library exception
            raise LLMGenerationError("OpenAI ChatCompletion API call failed") from exc

        choices = completion.get("choices") or []
        if not choices:
            raise LLMGenerationError("No choices returned from ChatCompletion API")
        message = choices[0].get("message", {})
        content = message.get("content", "")
        if not content:
            raise LLMGenerationError("Empty response from ChatCompletion API")
        return str(content).strip()


SYSTEM_PROMPT = textwrap.dedent(
    """
ROLE
You are an independent, fact-based news analyst specializing in Middle East affairs, with an emphasis on Israel and the Palestinian territories. Maintain a strictly neutral tone, quantify bias, and cite sources transparently.

OBJECTIVITY & SOURCING
- Only rely on factual, non-controversial verification sources.
- Approved verification sources: Reuters, Associated Press, BBC News (newswire), The Economist, Wall Street Journal (news), Times of Israel, Haaretz reporting, Foreign Affairs, Council on Foreign Relations, RAND Corporation, Congressional Research Service, academic/peer-reviewed research.
- Never use or cite: Al Jazeera, the United Nations, Wikipedia, The Intercept, Middle East Eye, Electronic Intifada, or advocacy outlets.
- Flag any cited source from the article that is controversial or advocacy-oriented.

WRITING RULES
- Neutral, precise, fact-focused tone.
- No speculation, emotion, or personal opinion.
- Always fill every section requested.
- Cross-check claims against the approved verification list before scoring accuracy.
- Quantify accuracy, propaganda, and bias on 0–10 scales.
- Highlight missing context, unsupported claims, or potential misinformation.

OUTPUT STRUCTURE
Provide content only for sections 1–7 below. Each section must include the specified elements, tables, and scoring directives.
    """
)


USER_PROMPT_TEMPLATE = textwrap.dedent(
    """
Analyze the article below and produce sections 1–7 exactly as specified. Use the provided analysis date and file path metadata inside your response.

Context
- File analyzed: {relative_path}
- Date of analysis: {analysis_date}

Formatting Requirements
1. Article Summary — 3–5 sentences, neutral tone, only core facts.
2. Accuracy Assessment — Describe verification process, missing context, or disputes. End with `Accuracy Score: <0-10 integer>`.
3. Propaganda / Agenda Indicators — Identify any narrative techniques. End with the appropriate verdict line exactly as one of the following (choose one):
   - `✅ Not propaganda`
   - `⚠️ Some propaganda indicators`
   - `🚨 Strong propaganda indicators`
   Follow the verdict with `Propaganda Score: <0-10 integer>` on a new line.
4. Sources Cited by the Article’s Author — Markdown table with columns `Source | Controversial? | Explanation`. If no sources are cited, include a single row with `None listed`.
5. Source Bias Assessment (Toward Israel) — Markdown table with columns `Source | Bias Rating (0–10) | Bias Direction | Justification`. After the table add a line in the format `Bias Mean Score: X.X → <interpretation>`.
6. Analyst’s Own Sources for Verification — Bullet list of the approved sources you used (e.g., `- Reuters dispatch on Gaza ceasefire, 2025-11-08`). If you found no relevant verification sources, explain why.
7. Overall Summary Metrics — Markdown table with columns `Metric | Scale | Score | Interpretation` covering Accuracy, Propaganda, and Bias (Israel vs. Anti-Israel). After the table, add a sentence starting with `Interpretation:` summarizing what the scores mean.

Additional Instructions
- Treat bias scores as 0 = strongly anti-Israel, 5 = neutral, 10 = strongly pro-Israel.
- If the article cites any disallowed or advocacy outlets, mark them as controversial with an explanation.
- Never cite or rely on banned verification sources.
- Ensure every requested element is present with no placeholders.

Article Markdown
----------------
{article_content}
----------------
    """
)


class MiddleEastAnalysisAgent:
    """Agent that generates structured analyses for news articles."""

    def __init__(
        self,
        config: Optional[MiddleEastAnalysisConfig] = None,
        llm_client: Optional[LLMClient] = None
    ):
        self.config = config or MiddleEastAnalysisConfig()
        self.llm_client = llm_client or OpenAILLMClient(
            model=self.config.model,
            temperature=self.config.temperature
        )
        self.analysis_date = datetime.utcnow().date().isoformat()

    def run(self) -> None:
        """Execute the agent end-to-end."""
        if not self.config.input_dir.exists():
            raise AgentError(
                f"Input directory '{self.config.input_dir}' does not exist"
            )

        self._reset_output_dir()

        article_paths = sorted(self.config.input_dir.rglob("*.md"))
        if not article_paths:
            logger.warning("No markdown files found in %s", self.config.input_dir)
            return

        limit = self.config.limit
        if limit is not None:
            article_paths = article_paths[:limit]

        logger.info(
            "Starting analysis for %s articles using model %s",
            len(article_paths),
            self.config.model
        )

        for path in article_paths:
            try:
                self._process_article(path)
            except AgentError as exc:
                logger.error("Failed to process %s: %s", path, exc)

    def _reset_output_dir(self) -> None:
        """Delete all output content to guarantee a clean run."""
        output_dir = self.config.output_dir
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Reset analysis output directory at %s", output_dir)

    def _process_article(self, article_path: Path) -> None:
        """Generate and persist analysis for a single article."""
        relative_path = article_path.relative_to(self.config.input_dir)
        logger.info("Analyzing %s", relative_path)
        article_content = article_path.read_text(encoding="utf-8").strip()

        if not article_content:
            raise AgentError(f"Article {relative_path} is empty")

        body = self._build_placeholder_body() if self.config.dry_run else self._generate_body(
            relative_path, article_content
        )

        document = self._wrap_with_header(relative_path, body)
        self._write_output(relative_path, document)

    def _generate_body(self, relative_path: Path, article_content: str) -> str:
        """Call the language model with retry handling."""
        system_prompt = SYSTEM_PROMPT
        user_prompt = USER_PROMPT_TEMPLATE.format(
            relative_path=relative_path.as_posix(),
            analysis_date=self.analysis_date,
            article_content=article_content
        )

        attempts = 0
        last_error: Optional[Exception] = None
        while attempts < self.config.max_retries:
            attempts += 1
            try:
                response = self.llm_client.generate(system_prompt, user_prompt)
                if response:
                    return response.strip()
                raise LLMGenerationError("Received empty response from language model")
            except LLMGenerationError as exc:
                last_error = exc
                logger.warning(
                    "Attempt %s/%s failed for %s: %s",
                    attempts,
                    self.config.max_retries,
                    relative_path,
                    exc
                )
                time.sleep(self.config.retry_delay_seconds)
        raise AgentError(
            f"Exceeded maximum retries for {relative_path}: {last_error}"
        )

    def _wrap_with_header(self, relative_path: Path, body: str) -> str:
        """Attach the required header metadata to the LLM body."""
        header = textwrap.dedent(
            f"""
            📰 Article Analysis
            File analyzed: {relative_path.as_posix()}
            Date of analysis: {self.analysis_date}
            """
        ).strip()
        return f"{header}\n\n{body.strip()}\n"

    @staticmethod
    def _build_placeholder_body() -> str:
        """Return a placeholder body when running in dry-run mode."""
        placeholder_sections = [
            "1. Article Summary\nPending analysis.",
            "2. Accuracy Assessment\nPending analysis. Accuracy Score: 0",
            "3. Propaganda / Agenda Indicators\nPending analysis.\n⚠️ Some propaganda indicators\nPropaganda Score: 0",
            "4. Sources Cited by the Article’s Author\n| Source | Controversial? | Explanation |\n|--------|---------------|-------------|\n| Pending | Pending | Placeholder entry |",
            (
                "5. Source Bias Assessment (Toward Israel)\n"
                "| Source | Bias Rating (0–10) | Bias Direction | Justification |\n"
                "|--------|---------------------|----------------|--------------|\n"
                "| Pending | 5 | Neutral | Placeholder entry |\n\n"
                "Bias Mean Score: 5.0 → neutral placeholder"
            ),
            "6. Analyst’s Own Sources for Verification\n- Pending verification",
            textwrap.dedent(
                """
                7. Overall Summary Metrics
                | Metric | Scale | Score | Interpretation |
                |--------|-------|-------|----------------|
                | Accuracy | 0–10 | 0 | Pending |
                | Propaganda | 0–10 | 0 | Pending |
                | Bias (Israel vs. Anti-Israel) | 0–10 | 5 | Pending |

                Interpretation: Placeholder metrics pending analysis.
                """
            ).strip()
        ]
        return "\n\n".join(placeholder_sections)

    def _write_output(self, relative_path: Path, document: str) -> None:
        """Write the completed analysis document to the mirrored output location."""
        output_path = self.config.output_dir / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(document, encoding="utf-8")
        logger.info("Saved analysis to %s", output_path)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the analysis agent."""
    parser = argparse.ArgumentParser(
        description="Generate Middle East-focused analyses for news markdown files"
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("news_md"),
        help="Directory containing source markdown articles"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("news_analysis_md"),
        help="Directory where analysis markdown files will be written"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        help="OpenAI model name to use for analysis"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="Sampling temperature for the model"
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum number of retries on model failures"
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=5.0,
        help="Seconds to wait between retries"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Optional limit on the number of articles to process"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate placeholder files without calling the language model"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging verbosity"
    )
    return parser.parse_args()


def main() -> None:
    """CLI entry point for the analysis agent."""
    args = parse_args()
    setup_logging(log_level=args.log_level)

    config = MiddleEastAnalysisConfig(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        model=args.model,
        temperature=args.temperature,
        max_retries=args.max_retries,
        retry_delay_seconds=args.retry_delay,
        limit=args.limit,
        dry_run=args.dry_run
    )

    agent = MiddleEastAnalysisAgent(config=config)
    agent.run()


if __name__ == "__main__":  # pragma: no cover
    main()
