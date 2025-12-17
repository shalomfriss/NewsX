"""
Credential Management UI
Provides a GUI for managing API credentials for various news sources.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from typing import Dict, Optional, Callable
import logging
import os
import getpass

logger = logging.getLogger(__name__)


class CredentialManagerUI:
    """GUI for managing API credentials."""

    # API registration URLs for each news source
    API_REGISTRATION_URLS = {
        "newsapi": {
            "name": "NewsAPI",
            "url": "https://newsapi.org/register",
            "fields": ["api_key"],
            "description": "Access to 80,000+ news sources worldwide"
        },
        "guardian": {
            "name": "The Guardian",
            "url": "https://open-platform.theguardian.com/access/",
            "fields": ["api_key"],
            "description": "Guardian news and content API"
        },
        "nyt": {
            "name": "New York Times",
            "url": "https://developer.nytimes.com/get-started",
            "fields": ["api_key"],
            "description": "NYT Article Search and Top Stories API"
        },
        "bbc": {
            "name": "BBC News",
            "url": "https://www.bbc.co.uk/news",
            "fields": [],
            "description": "BBC RSS feeds (no API key required)"
        },
        "reuters": {
            "name": "Reuters",
            "url": "https://www.reuters.com",
            "fields": [],
            "description": "Reuters RSS feeds (no API key required)"
        },
        "ap": {
            "name": "Associated Press",
            "url": "https://developer.ap.org/",
            "fields": ["api_key"],
            "description": "AP news content API"
        },
        "politico": {
            "name": "Politico",
            "url": "https://www.politico.com/rss",
            "fields": [],
            "description": "Politico RSS feeds (no API key required)"
        },
        "the_hill": {
            "name": "The Hill",
            "url": "https://thehill.com",
            "fields": [],
            "description": "The Hill RSS feeds (no API key required)"
        },
        "bloomberg": {
            "name": "Bloomberg",
            "url": "https://www.bloomberg.com/professional/support/api-library/",
            "fields": ["api_key"],
            "description": "Bloomberg Terminal API (requires subscription)"
        },
        "wsj": {
            "name": "Wall Street Journal",
            "url": "https://www.dowjones.com/professional/",
            "fields": [],
            "description": "WSJ RSS feeds (subscription may be required)"
        },
        "npr": {
            "name": "NPR",
            "url": "https://www.npr.org/rss",
            "fields": [],
            "description": "NPR RSS feeds (no API key required)"
        },
        "cnn": {
            "name": "CNN",
            "url": "https://www.cnn.com/services/rss/",
            "fields": [],
            "description": "CNN RSS feeds (no API key required)"
        },
        "abc": {
            "name": "ABC News",
            "url": "https://abcnews.go.com/Site/page/rss",
            "fields": [],
            "description": "ABC News RSS feeds (no API key required)"
        },
        "cbs": {
            "name": "CBS News",
            "url": "https://www.cbsnews.com/rss/",
            "fields": [],
            "description": "CBS News RSS feeds (no API key required)"
        },
        "nbc": {
            "name": "NBC News",
            "url": "https://www.nbcnews.com/feeds",
            "fields": [],
            "description": "NBC News RSS feeds (no API key required)"
        },
        "pbs": {
            "name": "PBS NewsHour",
            "url": "https://www.pbs.org/newshour/feeds",
            "fields": [],
            "description": "PBS NewsHour RSS feeds (no API key required)"
        },
        "washington_post": {
            "name": "Washington Post",
            "url": "https://www.washingtonpost.com/rss-feeds",
            "fields": [],
            "description": "Washington Post RSS feeds (subscription may be required)"
        },
        "the_atlantic": {
            "name": "The Atlantic",
            "url": "https://www.theatlantic.com/feed/all/",
            "fields": [],
            "description": "The Atlantic RSS feeds (no API key required)"
        },
        "propublica": {
            "name": "ProPublica",
            "url": "https://www.propublica.org/feeds",
            "fields": [],
            "description": "ProPublica RSS feeds (no API key required)"
        }
    }

    def __init__(self, missing_sources: list, on_save: Optional[Callable] = None):
        """
        Initialize the credential manager UI.

        Args:
            missing_sources: List of source IDs that need credentials
            on_save: Callback function to execute when credentials are saved
        """
        self.missing_sources = missing_sources
        self.on_save = on_save
        self.credential_entries: Dict[str, Dict[str, tk.Entry]] = {}
        self.show_password_vars: Dict[str, tk.BooleanVar] = {}
        self.root = None
        self.status_label = None

    def show(self) -> Dict[str, Dict[str, str]]:
        """
        Display the credential manager window and return entered credentials.

        Returns:
            Dictionary of credentials keyed by source ID
        """
        # Check if GUI is available
        if not self._gui_available():
            logger.info("GUI not available, falling back to CLI input")
            return self._show_cli()
        
        self.root = tk.Tk()
        self.root.title("News Aggregator - API Credentials Setup")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Set minimum window size
        self.root.minsize(700, 500)

        # Create main container with scrollbar
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Header
        header_label = ttk.Label(
            main_frame,
            text="🔑 API Credentials Setup",
            font=("Arial", 18, "bold")
        )
        header_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

        # Count sources requiring credentials
        sources_needing_creds = [s for s in self.missing_sources
                                if self.API_REGISTRATION_URLS.get(s, {}).get("fields", [])]

        info_text = (
            f"Setting up API credentials for {len(sources_needing_creds)} source(s).\n"
            f"💡 Click the blue registration links to sign up and get your free API keys.\n"
            f"👁️  Use the 'Show' buttons to verify your API keys are entered correctly.\n"
            f"📝 Note: 14 other sources work via RSS without any setup!"
        )

        info_label = ttk.Label(
            main_frame,
            text=info_text,
            wraplength=850,
            justify=tk.LEFT,
            font=("Arial", 10)
        )
        info_label.grid(row=1, column=0, pady=(0, 10), sticky=tk.W)

        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="",
            font=("Arial", 9, "italic"),
            foreground="blue"
        )
        self.status_label.grid(row=2, column=0, pady=(0, 5), sticky=tk.W)

        # Create canvas with scrollbar for sources
        canvas = tk.Canvas(main_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=3, column=1, sticky=(tk.N, tk.S))

        main_frame.rowconfigure(3, weight=1)

        # Add credential entry for each missing source
        for idx, source_id in enumerate(self.missing_sources):
            self._create_source_section(scrollable_frame, source_id, idx)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, pady=(10, 0), sticky=(tk.E, tk.W))

        skip_button = ttk.Button(
            button_frame,
            text="⏭️  Skip for Now",
            command=self._on_skip
        )
        skip_button.pack(side=tk.LEFT, padx=5)

        save_button = ttk.Button(
            button_frame,
            text="💾 Save Credentials",
            command=self._on_save_credentials
        )
        save_button.pack(side=tk.RIGHT, padx=5)

        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.root.mainloop()

        return self.collected_credentials if hasattr(self, 'collected_credentials') else {}

    def _create_source_section(self, parent: ttk.Frame, source_id: str, index: int):
        """Create a credential entry section for a news source."""
        source_info = self.API_REGISTRATION_URLS.get(source_id, {})
        source_name = source_info.get("name", source_id.upper())

        # Frame for this source with prominent label
        source_frame = ttk.LabelFrame(
            parent,
            text=f"  {source_name}  ",
            padding="15"
        )
        source_frame.grid(row=index, column=0, pady=8, padx=5, sticky=(tk.W, tk.E))
        parent.columnconfigure(0, weight=1)

        # Description with icon
        desc_text = f"📰 {source_info.get('description', 'News source')}"
        desc_label = ttk.Label(
            source_frame,
            text=desc_text,
            foreground="#555555",
            font=("Arial", 9)
        )
        desc_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 8))

        # Registration link
        if source_info.get("url"):
            link_frame = ttk.Frame(source_frame)
            link_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

            link_label = ttk.Label(
                link_frame,
                text="🔗 Get your API key here: ",
                font=("Arial", 9, "bold")
            )
            link_label.pack(side=tk.LEFT)

            link_button = tk.Label(
                link_frame,
                text=source_info["url"],
                foreground="#0066cc",
                cursor="hand2",
                font=("Arial", 9, "underline")
            )
            link_button.pack(side=tk.LEFT)
            link_button.bind(
                "<Button-1>",
                lambda e, url=source_info["url"], name=source_name: self._open_link(url, name)
            )

        # Credential fields
        fields = source_info.get("fields", [])
        if not fields:
            no_key_label = ttk.Label(
                source_frame,
                text="✅ No API key required - uses RSS feeds",
                foreground="green",
                font=("Arial", 10, "bold")
            )
            no_key_label.grid(row=2, column=0, columnspan=3, sticky=tk.W)
        else:
            self.credential_entries[source_id] = {}
            for field_idx, field_name in enumerate(fields):
                # Field label
                field_label = ttk.Label(
                    source_frame,
                    text=f"{field_name.replace('_', ' ').title()} *",
                    font=("Arial", 9, "bold")
                )
                field_label.grid(row=2 + field_idx, column=0, sticky=tk.W, pady=5)

                # Entry field
                entry_frame = ttk.Frame(source_frame)
                entry_frame.grid(row=2 + field_idx, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))

                field_entry = ttk.Entry(entry_frame, width=50, show="*" if "key" in field_name else "")
                field_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

                # Add placeholder text hint
                field_entry.insert(0, "Paste your API key here")
                field_entry.config(foreground="gray")

                def on_focus_in(event, entry=field_entry):
                    if entry.get() == "Paste your API key here":
                        entry.delete(0, tk.END)
                        entry.config(foreground="black")

                def on_focus_out(event, entry=field_entry):
                    if not entry.get():
                        entry.insert(0, "Paste your API key here")
                        entry.config(foreground="gray")

                field_entry.bind("<FocusIn>", on_focus_in)
                field_entry.bind("<FocusOut>", on_focus_out)

                # Show/Hide button for password fields
                if "key" in field_name or "password" in field_name:
                    show_var = tk.BooleanVar(value=False)
                    self.show_password_vars[f"{source_id}_{field_name}"] = show_var

                    def toggle_password(entry=field_entry, var=show_var, button=None):
                        if var.get():
                            entry.config(show="")
                            if button:
                                button.config(text="🔒 Hide")
                        else:
                            entry.config(show="*")
                            if button:
                                button.config(text="👁️  Show")

                    show_button = ttk.Button(
                        entry_frame,
                        text="👁️  Show",
                        width=9,
                        command=lambda e=field_entry, v=show_var, b=None: toggle_password(e, v, show_button)
                    )
                    show_button.pack(side=tk.LEFT, padx=(5, 0))

                self.credential_entries[source_id][field_name] = field_entry

        source_frame.columnconfigure(1, weight=1)

    def _open_link(self, url: str, source_name: str):
        """Open registration link and update status."""
        webbrowser.open(url)
        self._update_status(f"Opening registration page for {source_name}...")

    def _update_status(self, message: str, color: str = "blue"):
        """Update the status label with a message."""
        if self.status_label:
            self.status_label.config(text=message, foreground=color)
            self.root.update()

    def _on_save_credentials(self):
        """Handle save button click."""
        self._update_status("📝 Validating credentials...", "blue")

        self.collected_credentials = {}
        credentials_count = 0

        # Collect credentials from form
        for source_id, entries in self.credential_entries.items():
            source_creds = {}
            for field_name, entry_widget in entries.items():
                value = entry_widget.get().strip()
                # Skip placeholder text
                if value and value != "Paste your API key here":
                    source_creds[field_name] = value

            if source_creds:
                self.collected_credentials[source_id] = source_creds
                credentials_count += 1

        # Validate that at least one credential was entered
        if not self.collected_credentials:
            self._update_status("⚠️  No credentials entered", "orange")
            result = messagebox.askyesno(
                "No Credentials Entered",
                "You haven't entered any credentials.\n\n"
                "You can still use 14 news sources that work via RSS without API keys.\n\n"
                "Do you want to skip credential setup for now?"
            )
            if not result:
                self._update_status("", "blue")
                return
            else:
                self._update_status("✅ Skipping credential setup", "green")
                self.root.quit()
                self.root.destroy()
                return

        # Show what will be saved
        source_names = []
        for source_id in self.collected_credentials.keys():
            source_info = self.API_REGISTRATION_URLS.get(source_id, {})
            source_names.append(source_info.get("name", source_id))

        self._update_status(f"💾 Saving credentials for {credentials_count} source(s)...", "blue")

        # Save credentials
        if self.on_save:
            try:
                self.on_save(self.collected_credentials)
                self._update_status("✅ Credentials saved successfully!", "green")
            except Exception as e:
                self._update_status(f"❌ Failed to save credentials", "red")
                messagebox.showerror(
                    "Error Saving Credentials",
                    f"Failed to save credentials:\n\n{str(e)}\n\n"
                    f"Please try again or check the error logs."
                )
                logger.error(f"Failed to save credentials: {e}", exc_info=True)
                return

        # Success message
        success_msg = f"✅ Successfully saved credentials for:\n\n"
        for name in source_names:
            success_msg += f"  • {name}\n"
        success_msg += f"\n{len(source_names)} API source(s) are now configured!"

        messagebox.showinfo("Success!", success_msg)

        self.root.quit()
        self.root.destroy()

    def _on_skip(self):
        """Handle skip button click."""
        result = messagebox.askyesno(
            "Skip Credential Setup?",
            "Are you sure you want to skip credential setup?\n\n"
            "✅ You can still use 14 news sources via RSS (no API keys needed):\n"
            "   BBC, Reuters, AP, Politico, The Hill, NPR, CNN, ABC, CBS,\n"
            "   NBC, PBS, Washington Post, The Atlantic, ProPublica\n\n"
            "❌ API-based sources will not be available:\n"
            "   NewsAPI, The Guardian, New York Times\n\n"
            "You can always add credentials later by running:\n"
            "   python main.py --setup-credentials"
        )
        if result:
            self._update_status("⏭️  Skipping credential setup", "orange")
            self.collected_credentials = {}
            self.root.quit()
            self.root.destroy()

    def _gui_available(self) -> bool:
        """Check if GUI (Tkinter) is available."""
        try:
            # Check if DISPLAY is set on Unix-like systems
            if os.name != 'nt' and not os.environ.get('DISPLAY'):
                return False
            
            # Try to create a Tk instance
            test_root = tk.Tk()
            test_root.withdraw()
            test_root.destroy()
            return True
        except Exception as e:
            logger.debug(f"GUI not available: {e}")
            return False

    def _show_cli(self) -> Dict[str, Dict[str, str]]:
        """Command-line interface for credential management."""
        self.collected_credentials = {}
        
        print("\n" + "=" * 80)
        print("🔑 NEWS AGGREGATOR - API CREDENTIALS SETUP")
        print("=" * 80)
        
        # Count sources requiring credentials
        sources_needing_creds = [s for s in self.missing_sources
                                if self.API_REGISTRATION_URLS.get(s, {}).get("fields", [])]
        
        print(f"\nSetting up API credentials for {len(sources_needing_creds)} source(s).")
        print("💡 Visit the registration URLs below to sign up and get your free API keys.")
        print("📝 Note: 14 other sources work via RSS without any setup!\n")
        
        # Process each source
        for source_id in self.missing_sources:
            source_info = self.API_REGISTRATION_URLS.get(source_id, {})
            source_name = source_info.get("name", source_id.upper())
            fields = source_info.get("fields", [])
            
            print("\n" + "-" * 80)
            print(f"📰 {source_name}")
            print("-" * 80)
            print(f"Description: {source_info.get('description', 'News source')}")
            
            if not fields:
                print("✅ No API key required - uses RSS feeds")
                continue
            
            print(f"\n🔗 Get your API key here: {source_info.get('url', 'N/A')}")
            print(f"\nEnter credentials for {source_name} (press Enter to skip):")
            
            source_creds = {}
            for field_name in fields:
                field_label = field_name.replace('_', ' ').title()
                
                # Use getpass for sensitive fields, but fall back to input if not on TTY
                try:
                    if "key" in field_name.lower() or "password" in field_name.lower():
                        if os.isatty(0):  # Check if stdin is a terminal
                            value = getpass.getpass(f"  {field_label}: ").strip()
                        else:
                            value = input(f"  {field_label}: ").strip()
                    else:
                        value = input(f"  {field_label}: ").strip()
                except (EOFError, KeyboardInterrupt):
                    value = ""
                
                if value:
                    source_creds[field_name] = value
            
            if source_creds:
                self.collected_credentials[source_id] = source_creds
                print(f"✅ Credentials entered for {source_name}")
            else:
                print(f"⏭️  Skipped {source_name}")
        
        # Summary
        print("\n" + "=" * 80)
        if self.collected_credentials:
            print(f"💾 Saving credentials for {len(self.collected_credentials)} source(s)...")
            
            # Save credentials
            if self.on_save:
                try:
                    self.on_save(self.collected_credentials)
                    print("✅ Credentials saved successfully!")
                    
                    print("\nConfigured sources:")
                    for source_id in self.collected_credentials.keys():
                        source_name = self.API_REGISTRATION_URLS.get(source_id, {}).get("name", source_id)
                        print(f"  • {source_name}")
                except Exception as e:
                    print(f"❌ Failed to save credentials: {e}")
                    logger.error(f"Failed to save credentials: {e}", exc_info=True)
        else:
            print("⏭️  No credentials entered - you can still use RSS-based sources")
        
        print("=" * 80 + "\n")
        
        return self.collected_credentials


def show_credential_manager(missing_sources: list, on_save: Optional[Callable] = None) -> Dict[str, Dict[str, str]]:
    """
    Convenience function to show the credential manager.

    Args:
        missing_sources: List of source IDs that need credentials
        on_save: Optional callback when credentials are saved

    Returns:
        Dictionary of collected credentials
    """
    manager = CredentialManagerUI(missing_sources, on_save)
    return manager.show()
