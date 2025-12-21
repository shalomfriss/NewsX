# How We Created a Tool That Tells You Where Your Generic Drugs Were Made

**Source:** propublica
**Published:** 2025-12-18 15:00:00 UTC
**URL:** https://www.propublica.org/article/rx-inspector-fda-generic-drug-tool-methodology
**Author:** Ken Schwencke
**Categories:** Health Care
**Keywords:** Health Care

## Summary

<p>The post <a href="https://www.propublica.org/article/rx-inspector-fda-generic-drug-tool-methodology">How We Created a Tool That Tells You Where Your Generic Drugs Were Made</a> appeared first on <a href="https://www.propublica.org">ProPublica</a>.</p>

## Content

<p>To understand how risky drugs could end up in your medicine cabinet, ProPublica spent more than a year and a half <a href="https://www.propublica.org/article/fda-drug-loophole-sun-pharma">investigating the Food and Drug Administration’s oversight of the foreign factories</a> that make generic medications and have been cited for violating critical quality standards.</p>



<p>It quickly became clear through our reporting that patients and doctors don’t reliably have the information they need to make informed decisions about the medicines they take or prescribe.</p>



<p>ProPublica has created Rx Inspector, a tool that aims to help.&nbsp;</p>



<p>You can look up your generic prescription drugs, and we’ll guide you to the specific facility that made them. We were able to link more than 80% of generic prescription drug products in our database to a factory that made them using databases of label information, manufacturing facilities and location data that we sued the FDA for. Additionally, we included the history of FDA actions at those facilities based on a trove of inspection records we assembled.</p>



<p>Keep in mind that if you turn up a troubling inspection report, it doesn’t necessarily mean that your drug is compromised. Doctors and pharmacists advise that you not stop taking your medications. Instead, you should talk to your health care provider about any concerns.</p>



<p><a href="https://projects.propublica.org/rx-inspector/"><strong>Look up your prescriptions using the tool here.</strong></a></p>



<p>Our ongoing reporting has focused on the safety of generic drugs, which represent <a href="https://www.fda.gov/drugs/buying-using-medicine-safely/generic-drugs">the vast majority</a> of all prescriptions filled in the United States. Thus, Rx Inspector does not include brand-name or over-the-counter drugs, at least for now. We excluded gases (like oxygen tanks) and intradermal route drugs (many of these were allergy tests for things like feline hair).</p>



<p>ProPublica described the app and the methodology used to build it to the FDA, which did not comment. The agency previously told ProPublica that it doesn’t reveal where drugs are made on inspection reports to protect what it deemed confidential commercial information.</p>



<p>Here’s how we did it:</p>



<h3 class="wp-block-heading">Getting Lists of Drugs and Facilities</h3>



<p>First, we needed to get a list of prescription drugs. We downloaded the <a href="https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory">National Drug Code</a> product list from the FDA. A company that wants to make a generic must file an Abbreviated New Drug Application for approval. We used those ANDA numbers to filter our list to generic drugs only.&nbsp;</p>



<p>We included biological drug products, such as insulin. We opted to include <a href="https://www.fda.gov/drugs/abbreviated-new-drug-application-anda/fda-list-authorized-generic-drugs">authorized generics</a>, which are brand-name drugs that are marketed without the brand-name label, because we thought consumers may not know their “generic” is actually a brand-name drug.</p>



<p>We then joined that list of drugs to the <a href="https://dailymed.nlm.nih.gov/dailymed/">Structured Product Labeling</a> database from DailyMed, a National Institutes of Health resource that contains information on more than 155,000 drug labels submitted to the FDA by companies. We used that data to get basic information about the drugs, like the form (pill, injectable, etc.), dose, color, imprints and more. In some, but not all, cases, it also contained identifiers or addresses that we could use to link to the agency’s official list of manufacturing locations.&nbsp;</p>



<p>We then matched the drugs to three different facility lists:</p>



<p>The first and primary list comes from the FDA’s <a href="https://www.fda.gov/drugs/guidance-compliance-regulatory-information/electronic-drug-registration-and-listing-system-edrls">Electronic Drug Registration and Listing System</a>. That database contains the addresses of drugmakers’ factories. It also has two numeric identifiers: the FDA Establishment Identifier and a Dun &amp; Bradstreet, or DUNS, number.</p>



<p>The second facility list comes from a federal lawsuit we filed against the FDA for a list of manufacturer addresses connected to their ANDA numbers among other information. We received a partial list, which we used when we only had ANDA numbers for a drug.&nbsp;</p>



<p>And finally, we have a list of <a href="https://www.fda.gov/industry/generic-drug-user-fee-amendments/generic-drug-facilities-sites-and-organization-lists">historical facilities</a>, which allows us to identify production sites and link to them via FEI number if other routes don’t work.</p>



<h3 class="wp-block-heading">Joining Them Together</h3>



<p>In October, we detailed our unsuccessful search for the original manufacturer of a popular cholesterol generic through <a href="https://www.propublica.org/article/fda-transparency-atorvastatin-prescription-explainer">a labyrinth of company names and complex databases</a> that few consumers would even know exist. We decided we had to do something similar for nearly 47,000 drug products.&nbsp;&nbsp;</p>



<p>Different datasets had varying identifiers, and we had to link multiple together to find the correct facilities. For example, if all we had was an ANDA number, we used the facility list we obtained from our lawsuit, which also was listed by ANDA. If we had an FEI, we could link it to the FDA’s official list of facilities.&nbsp;</p>



<p>Sometimes, we had neither. In cases where we did not have any useful identifiers, we searched the product labeling data for any manufacturing addresses and attempted to match them to our facility lists. We used both fuzzy text matching and geocoding to do this and then manually reviewed our matches.&nbsp;</p>



<p>For repackaged or relabeled drugs, we traced back to the original label using the source NDC code.</p>



<p>In total, we were able to match more than 39,250 products to a manufacturing facility.</p>



<h3 class="wp-block-heading">Getting the Inspection Data&nbsp;</h3>



<p>Linking up individual drugs was only half the battle. The next thing we did was acquire the FDA’s inspection outcomes for facilities and join them back to our facility lists.&nbsp;</p>



<p>We acquired data on FDA inspections from a variety of sources. First, we turned to the FDA’s <a href="https://datadashboard.fda.gov/oii/cd/inspections.htm">public inspections dashboard</a> for inspections since 2008. We used only information related to drugs or biologics, excluding inspections related to food, cosmetics, tobacco, medical devices and veterinary products. This dashboard contained the dates and outcomes of inspections, as well as citations detailing any violations of federal code. We linked these reports back to a facility with a matching FEI number.</p>



<p>That still only gave us limited information for inspections. For documents with more details, we needed what’s known as a Form 483, which is where inspectors document problems they observe at a facility. Unfortunately, the FDA does not make all 483s public. We began by exporting those that have been published in the inspections dashboard, though we know this is incomplete.</p>



<p>We also went directly to the FDA and asked for all the 483s that had already been released publicly. They delivered a trove of almost 40,000 documents.</p>



<p>We linked the 483s to an inspection by extracting text from the documents using optical character recognition, connecting them to a facility using the FEI number and finding inspections of that facility within 10 days of the date of the letter. We were unable to link every 483 to an inspection because the FDA’s public inspections data does not include every inspection the agency conducts.&nbsp;</p>



<p>The FDA publishes <a href="https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/about-warning-and-close-out-letters">warning letters</a> that detail “significant violation(s) of federal requirement(s).” We obtained these from the FDA’s website going back to 2020, filtered out the ones not related to drugs and connected the rest to a facility using the FEI number.&nbsp;</p>



<p>Some facilities are outright banned from sending drugs to the U.S. market for a time, with exceptions for certain drugs as ProPublica detailed in <a href="https://www.propublica.org/series/rx-roulette">reporting this year</a>. The FDA calls this an import alert.</p>



<p>We used the Internet Archive’s Wayback Machine to find hundreds of import alert lists published by the FDA over more than 15 years. The lists identified factories banned from shipping drugs to the United States because the FDA found manufacturing violations.&nbsp;</p>



<p>We focused on <a href="https://www.accessdata.fda.gov/cms_ia/importalert_189.html">66-40 alerts</a>, which call out drug manufacturing facilities that do not meet “good manufacturing practice” standards. We considered the published date on the alert as the start date. We are unable to tell when an alert was lifted and instead approximate it using the date we last see the facility on the list. Import alerts do not include FEI numbers to easily identify the facility in question, so we used the entity name and address to tie them back to a facility.</p>



<p>We attempted to identify exemptions to import alerts by looking for strings like “excluded from DWPE” (“detention without physical examination”), then parse it manually to get a clean list of drugs.</p>



<p>To support our research, we paid for access to <a href="https://redica.com/">Redica Systems</a>, a quality and regulatory intelligence company with a vast collection of FDA inspection documents. We used Redica’s database to spot-check our own work.</p>



<p>We know that much of the data represented here is likely an undercount. Clerical errors could have resulted in missed connections. The FDA sometimes removes inspection outcomes from its dashboard, and our method of scraping through the Internet Archive is subject to availability. We were also limited in how completely we could obtain 483s, warning letters and import alerts. There may be additional communications between the company and the FDA that are not reflected in our database because they have not been made public.&nbsp;</p>



<p>Still, this is the most comprehensive public list of FDA actions tied to drugs that has ever been assembled.</p>
<p>The post <a href="https://www.propublica.org/article/rx-inspector-fda-generic-drug-tool-methodology">How We Created a Tool That Tells You Where Your Generic Drugs Were Made</a> appeared first on <a href="https://www.propublica.org">ProPublica</a>.</p>