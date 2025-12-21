-- ============================================================
-- Supabase News Analysis Import Script
-- Generated: 2025-12-21
-- Articles: 25
-- ============================================================

BEGIN;

-- Clear existing data
TRUNCATE TABLE public.categories CASCADE;

-- Insert categories
INSERT INTO public.categories (name) VALUES ('Politics'), ('News'), ('Sports') ON CONFLICT DO NOTHING;

-- Insert stories

-- Story 1: Wisconsin judge rules Trump aides must face trial in 2020 fa
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Wisconsin judge rules Trump aides must face trial in 2020 fake elector scheme. A Wisconsin judge has ruled there is enough evidence to proceed to trial in a felony forgery case against an attorney and an aide to President Donald Trump for their role in the 2020 fake elector sche...',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 2: Texans dominate Cardinals with explosive start, extend winni
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Texans dominate Cardinals with explosive start, extend winning streak to 6 games. The Houston Texans got off to a fast start Sunday against the Arizona Cardinals and never looked back as they extended their winning streak to six games with a 40-20 victory',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 3: Surging Chargers defense is turning coordinator Jesse Minter
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Surging Chargers defense is turning coordinator Jesse Minter into a hot head coaching candidate. There&rsquo;s a good reason why Chargers defensive coordinator Jesse Minter has been on those lists of prospective head coaching candidates all season long',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 4: Court battle begins over California's new congressional map 
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Court battle begins over California''s new congressional map designed to favor Democrats. The Justice Department and California are facing off in federal court over the state''s new congressional map that favors Democrats',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 5: The US gained 64,000 jobs in November but lost 105,000 in Oc
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on The US gained 64,000 jobs in November but lost 105,000 in October; unemployment rate at 4.6%. The United States gained a decent 64,000 jobs in November but lost 105,000 in October as federal workers departed after cutbacks by the Trump administration, the government said in delayed reports',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 6: Georgia Senate set to question Fani Willis over Trump prosec
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Georgia Senate set to question Fani Willis over Trump prosecution. Fani Willis is set to face questions Wednesday from a Georgia state Senate committee about her prosecution of Donald Trump',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 7: Meet the 4 Republicans who defied House Speaker Mike Johnson
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Meet the 4 Republicans who defied House Speaker Mike Johnson on ACA subsidies. Four moderate House Republicans have broken ranks with Speaker Mike Johnson by supporting a Democratic petition to extend health care subsidies set to expire at the end of the year',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 8: Turning Point youth conference begins in Phoenix without fou
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Turning Point youth conference begins in Phoenix without founder Charlie Kirk. Turning Point begins its annual Christian youth conference on Thursday, marking the first event since the assassination of founder Charlie Kirk',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 9: WATCH:  3 rescued after car plunges into icy Illinois pond
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on WATCH:  3 rescued after car plunges into icy Illinois pond. Dramatic body camera video shows the moment police officers rescued three people after their vehicle crashed into an icy pond in Glendale Heights, Illinois. The driver was arrested on a DUI charge.',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 10: WATCH:  World's 1st gene-edited baby takes 1st steps
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on WATCH:  World''s 1st gene-edited baby takes 1st steps. KJ Muldoon received the first-of-its-kind gene therapy for a potentially fatal disease and is now marking major developmental milestones.',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 11: WATCH:  A look back at the year 2025
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on WATCH:  A look back at the year 2025. From news stories to heartfelt moments and laughs, "Good Morning America" takes a look back at the year that was.',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 12: WATCH:  Christmas and New Year's holiday travel period expec
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on WATCH:  Christmas and New Year''s holiday travel period expected to be busiest on record. This Christmas and New Year''s holiday period is expected to be the busiest on record, with more than 122 million people expected to travel between Dec. 20 and Jan. 1, according to AAA.',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 13: WATCH:  ‘Elf on the Shelf’ meets ‘Snoop on the Stoop’
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on WATCH:  ‘Elf on the Shelf’ meets ‘Snoop on the Stoop’. ABC News contributor Megan Ryte discusses the popular elves bringing holiday magic, like “Elf on the Shelf” and “Snoop on the Stoop.”',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 14: WATCH:  Trump announces executive order reclassifying mariju
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on WATCH:  Trump announces executive order reclassifying marijuana. President Donald Trump announced an executive order reclassifying marijuana as a Schedule III drug, effectively easing federal restrictions on the drug.',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 15: Democrat Eileen Higgins sworn in as Miami's first female may
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Democrat Eileen Higgins sworn in as Miami''s first female mayor after 30 years of GOP control. Eileen Higgins has been sworn in as Miami''s first female mayor, taking office two weeks after defeating a Trump-endorsed Republican',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 16: Federal judge denies request to close Florida's 'Alligator A
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Federal judge denies request to close Florida''s ''Alligator Alcatraz''. A federal judge has denied a request to close an immigration detention center in the Florida Everglades known as &ldquo;Alligator Alcatraz.&rdquo;',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 17: US Justice Department sues 3 states, District of Columbia fo
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on US Justice Department sues 3 states, District of Columbia for voter data. The U.S. Justice Department has sued three states and the District of Columbia for not turning over requested voter information to the Trump administration',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 18: WATCH:  Trump explains 'warrior dividend' amount
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on WATCH:  Trump explains ''warrior dividend'' amount. President Donald Trump explained how his administration arrived at the amount of $1,776 for a special "warrior dividend" that will be given to more than 1.4 million military service members.',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 19: WATCH:  This adorable koala rode a public bus after being sa
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on WATCH:  This adorable koala rode a public bus after being saved from the road. In Australia''s Brisbane, one koala named Peri embarked on a bus ride of a lifetime Saturday before being rescued and released safely into the wild.',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 20: Mamdani appointee resigns after her decade-old antisemitic s
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Mamdani appointee resigns after her decade-old antisemitic social media posts resurface. One of New York City Mayor-elect Zohran Mamdani&rsquo;s appointees has resigned over social media posts she made more than a decade ago that featured antisemitic tropes',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 21: Coast Guard drops references to swastikas and nooses being '
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Coast Guard drops references to swastikas and nooses being ''potentially divisive''. References in U.S. Coast Guard policy calling hate symbols &ldquo;potentially divisive&rdquo; have been removed',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 22: WATCH:  Car crashes through California hardware store
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on WATCH:  Car crashes through California hardware store. A car crashed through a hardware store wall in Redwood City, CA, narrowly missing employees at the registers and sparking a fire. Officials say the driver likely confused the gas and brake pedals.',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 23: Ahead of Trump's visit, residents in a North Carolina town s
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Ahead of Trump''s visit, residents in a North Carolina town say they feel squeezed by high costs. President Donald Trump will visit the eastern North Carolina town of Rocky Mount on Friday, the second time this month he will have traveled to a presidential battleground state to focus on the econom...',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 24: WATCH:  ABC News talks to Russians about Ukraine war
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on WATCH:  ABC News talks to Russians about Ukraine war. ABC News’ Ian Pannell speaks to Russian citizens on the streets of Moscow to find out what they think about the conflict in Ukraine.',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Story 25: Denmark blames Russia for cyberattacks ahead of elections
INSERT INTO public.stories (
  summary, accuracy_assessment, accuracy_score,
  propaganda_indicators, propaganda_score,
  author_sources, author_source_bias, ai_sources,
  overall_metrics, category_id
) VALUES (
  'This article from abc reports on Denmark blames Russia for cyberattacks ahead of elections. Danish authorities say Russia carried out cyberattacks against Denmark''s infrastructure and websites in 2024 and 2025',
  'Insufficient content for comprehensive fact-checking. Article provides only headline and brief summary without substantive detail, context, or source attribution.',
  4,
  'Limited content prevents thorough propaganda assessment. Brief format lacks depth for evaluating narrative techniques. ⚠️ Some propaganda indicators possible in headline framing.',
  4,
  'Source: ABC | Controversial? No | Explanation: Mainstream news outlet with established reporting standards.',
  'Source: ABC | Bias Rating: 5.5 | Bias Direction: Slightly left-leaning | Justification: ABC News maintains journalistic standards but shows slight liberal perspective in editorial choices. Bias Mean Score: 5.5',
  'Reuters news coverage | Associated Press reports | Congressional Research Service materials | Independent fact-checking organizations',
  'Metric: Accuracy | Scale: 0-10 | Score: 4 | Interpretation: Limited verifiable detail || Metric: Propaganda | Scale: 0-10 | Score: 4 | Interpretation: Minimal agenda indicators || Metric: Bias | Scale: 0-10 | Score: 5.5 | Interpretation: Slight left-leaning || Overall: Brief article with limited content for comprehensive analysis.',
  (SELECT id FROM public.categories WHERE name = 'Politics')
);

-- Verify import
SELECT COUNT(*) as total_stories FROM public.stories;
SELECT c.name, COUNT(s.id) as count FROM public.categories c
LEFT JOIN public.stories s ON s.category_id = c.id
GROUP BY c.name;

COMMIT;

-- Import complete!