

Combined HTML









Custom rule examples \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Custom%20rule%20examples%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* Custom rule examples
On this page* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Custom rule examples
====================


Not sure what to write a rule for? Below are some common questions, 
ideas, and topics to spur your imagination. Happy hacking! 💡


Use cases[​](#use-cases "Direct link to Use cases")
---------------------------------------------------


### Automate code review comments[​](#automate-code-review-comments "Direct link to Automate code review comments")


*Time to write this rule: **5 minutes***


You can use Semgrep and its GitHub integration to [automate PR comments](https://semgrep.dev/docs/semgrep-appsec-platform/notifications)
 that you frequently make in code reviews. Writing a custom rule for the
 code pattern you want to target is usually straightforward. If you want
 to understand the Semgrep syntax, see the [documentation](https://semgrep.dev/docs/writing-rules/pattern-syntax) or try the [tutorial](https://semgrep.dev/learn).


![A reviewer writes a Semgrep rule and adds it to an organization-wide policy](Custom%20rule%20examples%20_%20Semgrep_files/semgrep-ci-4c94be66f30fef156679254592d3e2b1.gif)


  

A reviewer writes a Semgrep rule and adds it to an organization\-wide policy.


### Ban dangerous APIs[​](#ban-dangerous-apis "Direct link to Ban dangerous APIs")


*Time to write this rule: **5 minutes***


Semgrep can detect dangerous APIs in code. If integrated into CI/CD 
pipelines, you can use Semgrep to block merges or flag for review when 
someone adds such dangerous APIs to the code. For example, a rule that 
detects React's `dangerouslySetInnerHTML` looks like this.



### Exempting special cases of dangerous APIs[​](#exempting-special-cases-of-dangerous-apis "Direct link to Exempting special cases of dangerous APIs")


*Time to write this rule: **5 minutes***


If you have a legitimate use case for a dangerous API, you can exempt a specific use of the API using a `nosemgrep` comment. The rule below checks for React's `dangerouslySetInnerHTML`, but the code is annotated with a `nosemgrep` comment. Semgrep will not detect this line. This allows Semgrep to continuously check for future uses of `dangerouslySetInnerHTML` while allowing for this specific use.



### Detect tainted data flowing into a dangerous sink[​](#detect-tainted-data-flowing-into-a-dangerous-sink "Direct link to Detect tainted data flowing into a dangerous sink")


*Time to write this rule: **5 minutes***


Semgrep's [dataflow engine with support for taint tracking](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview) can be used to detect when data flows from a user\-provided value into a security\-sensitive function.


This rule detects when a user of the ExpressJS framework passes user data into the `run()` method of a sandbox.



### Detect security violations[​](#detect-security-violations "Direct link to Detect security violations")


*Time to write this rule: **5 minutes***


Use Semgrep to flag specific uses of APIs too, not just their 
presence in code. We jokingly call these the "security off" buttons and 
make extensive use of Semgrep to detect them.


This rule detects when HTML auto escaping is explicitly disabled for a Django template.



### Scan configuration files using JSON, YAML, or Generic pattern matching[​](#scan-configuration-files-using-json-yaml-or-generic-pattern-matching "Direct link to Scan configuration files using JSON, YAML, or Generic pattern matching")


*Time to write this rule: **10 minutes***


Semgrep [natively supports JSON and YAML](https://semgrep.dev/docs/supported-languages) and can be used to write rules for configuration files. This rule checks for skipped TLS verification in Kubernetes clusters.



The [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
 mode is for languages and file formats that Semgrep does not natively 
support. For example, you can write rules for Dockerfiles using the 
generic mode. The Dockerfile rule below checks for invalid port numbers.



### Enforce authentication patterns[​](#enforce-authentication-patterns "Direct link to Enforce authentication patterns")


*Time to write this rule: **15 minutes***


If a project has a "correct" way of doing authentication, Semgrep can
 be used to enforce this so that authentication mishaps do not happen. 
In the example below, this Flask app requires an authentication 
decorator on all routes. The rule detects routes that are missing 
authentication decorators. If deployed in CI/CD pipelines, Semgrep can 
block undecorated routes or flag a security member for further 
investigation.



### Systematize project\-specific coding patterns[​](#systematize-project-specific-coding-patterns "Direct link to Systematize project-specific coding patterns")


*Time to write this rule: **10 minutes***


Automate institutional knowledge using Semgrep. This has several 
benefits, including teaching new members about coding patterns in an 
automatic way and keeping a project up\-to\-date with coding patterns. If 
you keep coding guidelines in a document, converting these into Semgrep 
rules is a great way to free developers from having to remember all the 
guidelines.


In this example, a legacy API requires calling `verify_transaction(t)` before calling `make_transaction(t)`. The Semgrep rule below detects when these methods are not called correctly.



### Extract information with metavariables[​](#extract-information-with-metavariables "Direct link to Extract information with metavariables")


*Time to write this rule: **15 minutes***


Semgrep metavariables can be used as output in the `message` key. This can be used to extract and collate information about a codebase. Click through to [this example](https://semgrep.dev/s/ORpk) which extracts Java Spring routes. This can be used to quickly see all the exposed routes of an application.


### Burn down deprecated APIs[​](#burn-down-deprecated-apis "Direct link to Burn down deprecated APIs")


*Time to write this rule: **5 minutes***


Semgrep can detect deprecated APIs just as easily as dangerous APIs. 
Identifying deprecated API calls can help an application migrate to 
current or future versions.


This rule example detects a function that is deprecated as of Django 4\.0\.



### Promote secure alternatives[​](#promote-secure-alternatives "Direct link to Promote secure alternatives")


*Time to write this rule: **5 minutes***


Some libraries or APIs have safe alternatives, such as [Google's `re2`](https://github.com/google/re2), an implementation of the standard `re` interface that ships with Python that is resistant to regular expression denial\-of\-service. This rule detects the use of `re` and recommends `re2` as a safe alternative with the same interface.



Prompts for writing custom rules[​](#prompts-for-writing-custom-rules "Direct link to Prompts for writing custom rules")
------------------------------------------------------------------------------------------------------------------------


Try answering these questions to uncover important rules for your project.


1. From recent post mortems: what code issues contributed to it?
2. \[XYZ] is a (security, performance, other) library that everyone should use, but they don’t consistently.
3. When you review code, what changes do you frequently ask for?
4. What vulnerability classes from bug bounty submissions reoccur (or appear in different places of the codebase)?
5. Are there engineering or performance patterns? Consistent exception handlers?
6. What issues were caused by misconfigurations in Infrastructure\-as\-Code files (JSON)?
7. What are some “invariants” that should hold about your code \- things
 that should always or never be true (e.g. every admin route checks if 
user is admin)?
8. What methods/APIs are deprecated and you’re trying to move away from?


---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/rule-ideas.md)Last updated on **Jun 12, 2024**[PreviousPattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)[NextRule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)* [Use cases](#use-cases)
	+ [Automate code review comments](#automate-code-review-comments)
	+ [Ban dangerous APIs](#ban-dangerous-apis)
	+ [Exempting special cases of dangerous APIs](#exempting-special-cases-of-dangerous-apis)
	+ [Detect tainted data flowing into a dangerous sink](#detect-tainted-data-flowing-into-a-dangerous-sink)
	+ [Detect security violations](#detect-security-violations)
	+ [Scan configuration files using JSON, YAML, or Generic pattern matching](#scan-configuration-files-using-json-yaml-or-generic-pattern-matching)
	+ [Enforce authentication patterns](#enforce-authentication-patterns)
	+ [Systematize project\-specific coding patterns](#systematize-project-specific-coding-patterns)
	+ [Extract information with metavariables](#extract-information-with-metavariables)
	+ [Burn down deprecated APIs](#burn-down-deprecated-apis)
	+ [Promote secure alternatives](#promote-secure-alternatives)
* [Prompts for writing custom rules](#prompts-for-writing-custom-rules)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Custom%20rule%20examples%20_%20Semgrep_files/adsct_002.gif)![](Custom%20rule%20examples%20_%20Semgrep_files/adsct.gif)









Private rules \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Private%20rules%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* Private rules
On this page* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Private rules
=============


Users of the [Team or Enterprise tier](https://semgrep.dev/pricing) of Semgrep Code can publish rules to the [Semgrep Registry](https://semgrep.dev/explore)
 as private rules that are not visible to others outside their 
organization. Maintaining the rules' privacy allows you the benefits of 
using the Semgrep Registry while keeping sensitive code or information 
internal.


Creating private rules[​](#creating-private-rules "Direct link to Creating private rules")
------------------------------------------------------------------------------------------


Create private rules the same way you create other custom rules. 
Private rules are stored in Semgrep Registry but they are not visible 
outside your organization. The two sections below can help you to create
 and save your private rules.


Prerequisite[Team or Enterprise tier](https://semgrep.dev/pricing) of Semgrep Code.


### Creating private rules through Semgrep AppSec Platform[​](#creating-private-rules-through-semgrep-appsec-platform "Direct link to Creating private rules through Semgrep AppSec Platform")


To publish private rules through the Semgrep AppSec Platform:


1. Go to [Semgrep Editor](https://semgrep.dev/orgs/-/editor).
2. Click  **Create New Rule**.
3. Choose one of the following:
	* Create a new rule and test code by clicking  **plus** icon, select **New rule**, and then click  **Save**.
	* In the  **Library** panel, select a rule from a category in **Semgrep Registry**. Click  **Fork**, modify the rule or test code, and then click  **Save**.
4. Click  **Share**.
5. Click  **Private**.


Your private rule has been created and added to the Registry, visible
 only to logged in users of your organization. Its private status is 
reflected by the **Share** button displaying a  icon.


Private rules are stored in the folder with the same name as your Semgrep AppSec Platform organization.


### Creating private rules through the command line[​](#creating-private-rules-through-the-command-line "Direct link to Creating private rules through the command line")


To create private rules through the [Semgrep CLI](https://semgrep.dev/docs/getting-started/quickstart), :


1. Interactively login to Semgrep:



```
semgrep login  

```
2. Create your rule. For more information, see [Contributing rules](https://semgrep.dev/docs/contributing/contributing-to-semgrep-rules-repository) documentation.
3. Publish your rule from the command line with `semgrep publish` command followed by the path to your private rules:



```
semgrep publish myrules/  

```


If the rules are in the directory you publish from, you can use `semgrep publish .` to refer to the current directory. You must provide the directory specification.
If the directory contains test cases for the rules, Semgrep uploads them as well (see [testing Semgrep rules](https://semgrep.dev/docs/writing-rules/testing-rules)).


You can also change the visibility of the rules. For instance, to 
publish the rules as unlisted (which does not require authentication but
 will not be displayed in the public registry):



```
semgrep publish --visibility=unlisted myrules/  

```

For more details, run `semgrep publish --help`.


Viewing and using private rules[​](#viewing-and-using-private-rules "Direct link to Viewing and using private rules")
---------------------------------------------------------------------------------------------------------------------


View your rule in the [editor](https://semgrep.dev/orgs/-/editor) under the folder corresponding to your organization name.


You can also find it in the [registry](https://semgrep.dev/explore) by searching for \[organization\-id].\[rule\-id]. For example: `r2c.test-rule-id`.


To enforce the rule on new scans, add the rule in the [registry](https://semgrep.dev/explore) to an existing policy.


Automatically publishing rules[​](#automatically-publishing-rules "Direct link to Automatically publishing rules")
------------------------------------------------------------------------------------------------------------------


This section provides examples of how to automatically publish your 
private rules so they are accessible within your private organization. 
"Publishing" your private rules in this manner does not make them 
public. In the following examples, the private rules are stored in `private_rule_dir`,
 which is a subdirectory of the repository root. If your rules are in 
the root of your repository, you can replace the command with `semgrep publish --visibility=org_private .` to refer to the repository root. You must provide the directory specification.


The following sample of the GitHub Actions workflow publishes rules from a private Git repository after a merge to the `main`, `master`, or `develop` branches.


1. Make sure that `SEMGREP_APP_TOKEN` is defined in your GitHub project or organization's secrets.
2. Create the following file at `.github/workflows/semgrep-publish.yml`:



```
name: semgrep-publish  
  
on:  
  push:  
    branches:  
    - main  
    - master  
    - develop  
  
jobs:  
  publish:  
    name: publish-private-semgrep-rules  
    runs-on: ubuntu-latest  
    container:  
      image: semgrep/semgrep  
    steps:  
    - uses: actions/checkout@v4  
    - name: publish private semgrep rules  
      run: semgrep publish --visibility=org_private ./private_rule_dir  
      env:  
        SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}  

```

A sample job for GitLab CI/CD:



```
semgrep-publish:  
  image: semgrep/semgrep  
  script: semgrep publish --visibility=org_private ./private_rule_dir  
  
rules:  
  - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH  
  
variables:  
  SEMGREP_APP_TOKEN: $SEMGREP_APP_TOKEN  

```

Ensure that `SEMGREP_APP_TOKEN` is defined in your GitLab project's CI/CD variables.


Deleting private rules[​](#deleting-private-rules "Direct link to Deleting private rules")
------------------------------------------------------------------------------------------


To remove a private rule, follow these steps:


1. In the [Semgrep Editor](https://semgrep.dev/orgs/-/editor), find a private rule to delete under the  **Library** tab. Private rules are usually stored in the folder with the same name as your Semgrep AppSec Platform organization.
2. Click the rule you want to delete, and then click the  three vertical dots.
3. Click  **Delete**.


Deleting a rule is permanent. If the rule was previously added to the Policies page, it is removed upon deletion.


Appendix[​](#appendix "Direct link to Appendix")
------------------------------------------------


### Visibility of private rules[​](#visibility-of-private-rules "Direct link to Visibility of private rules")


Private rules are only visible to logged\-in members of your organization.


### Publishing a rule with the same rule ID[​](#publishing-a-rule-with-the-same-rule-id "Direct link to Publishing a rule with the same rule ID")


Rules have unique IDs. If you publish a rule with the same ID as an existing rule, the new rule overwrites the previous one.



---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/private-rules.md)Last updated on **Jun 12, 2024**[PreviousTesting rules](https://semgrep.dev/docs/writing-rules/testing-rules)[NextAutofix](https://semgrep.dev/docs/writing-rules/autofix)* [Creating private rules](#creating-private-rules)
	+ [Creating private rules through Semgrep AppSec Platform](#creating-private-rules-through-semgrep-appsec-platform)
	+ [Creating private rules through the command line](#creating-private-rules-through-the-command-line)
* [Viewing and using private rules](#viewing-and-using-private-rules)
* [Automatically publishing rules](#automatically-publishing-rules)
* [Deleting private rules](#deleting-private-rules)
* [Appendix](#appendix)
	+ [Visibility of private rules](#visibility-of-private-rules)
	+ [Publishing a rule with the same rule ID](#publishing-a-rule-with-the-same-rule-id)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Private%20rules%20_%20Semgrep_files/adsct_002.gif)![](Private%20rules%20_%20Semgrep_files/adsct.gif)









Metavariable analysis \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Metavariable%20analysis%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* Metavariable analysis
On this page* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Metavariable analysis
=====================


Metavariable analysis was created to support some metavariable 
inspection techniques that are difficult to express with existing rules 
but have "simple" binary classifier behavior. Currently, this syntax 
supports two analyzers: `redos` and `entropy`


ReDoS[​](#redos "Direct link to ReDoS")
---------------------------------------



```
metavariable-analysis:  
    analyzer: redos  
    metavariable: $VARIABLE  

```

RegEx denial of service is caused by poorly constructed regular 
expressions that exhibit exponential runtime when fed specifically 
crafted inputs. The `redos` analyzer uses known RegEx 
antipatterns to determine if the target expression is potentially 
vulnerable to catastrophic backtracking.



Entropy[​](#entropy "Direct link to Entropy")
---------------------------------------------



```
metavariable-analysis:  
    analyzer: entropy  
    metavariable: $VARIABLE  

```

Entropy is a common approach for detecting secret strings \- many 
existing tools leverage a combination of entropy calculations and RegEx 
for secret detection. This analyzer returns `true` if a metavariable has high entropy (randomness) relative to the English language.




---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/metavariable-analysis.md)Last updated on **Jun 12, 2024**[PreviousGeneric pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)[NextTroubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)* [ReDoS](#redos)
* [Entropy](#entropy)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Metavariable%20analysis%20_%20Semgrep_files/adsct_002.gif)![](Metavariable%20analysis%20_%20Semgrep_files/adsct.gif)









Testing rules \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Testing%20rules%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* Testing rules
On this page* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Testing rules
=============


Semgrep provides a convenient testing mechanism for your rules. You 
can simply write code and provide a few annotations to let Semgrep know 
where you are or aren't expecting findings. Semgrep provides the 
following annotations:


* `ruleid: <rule-id>`, for protecting against false negatives
* `ok: <rule-id>` for protecting against false positives
* `todoruleid: <rule-id>` for future "positive" rule improvements
* `todook: <rule-id>` for future "negative" rule improvements


Other than annotations there are three things to remember when creating tests:


1. The `--test` flag tells Semgrep to run tests in the specified directory.
2. Annotations are specified as a comment above the offending line.
3. Semgrep looks for tests based on the rule filename and the languages
specified in the rule. In other words, `path/to/rule.yaml` searches for
`path/to/rule.py`, `path/to/rule.js` and similar, based on the languages specified in the rule.


infoThe `.test.yaml` file extension can also be used for test files. This is necessary when testing YAML language rules.


Testing autofix[​](#testing-autofix "Direct link to Testing autofix")
---------------------------------------------------------------------


Semgrep's testing mechanism also provides a way to test the behavior of any `fix` values defined in the rules.


To define a test for autofix behavior:


1. Create a new **autofix test file** with the `.fixed` suffix before the file type extension.
For example, name the autofix test file of a rule with test code in `path/to/rule.py` as `path/to/rule.fixed.py`.
2. Within the autofix test file, enter the expected result of applied autofix rule to the test code.
3. Run `semgrep --test` to verify that your autofix test file is correctly detected.


When you use `semgrep --test`, Semgrep applies the autofix rule to the original test code (`path/to/rule.py`), and then verifies whether this matches the expected outcome defined in the autofix test file (`path/to/rule.fixed.py)`. If there is a mismatch, the line diffs are printed.


info**Hint**: Creating an autofix test for a rule with autofix can take less than a minute with the following flow of commands:


```
cp rule.py rule.fixed.py  
semgrep --config rule.yaml rule.fixed.py --autofix  

```
These
 commands apply the autofix of the rule to the test code. After Semgrep 
delivers a fix, inspect whether the outcome of this fix looks as 
expected (for example using `vimdiff rule.py rule.fixed.py`).


Example[​](#example "Direct link to Example")
---------------------------------------------


Consider the following rule:



```
rules:  
- id: insecure-eval-use  
  patterns:  
  - pattern: eval($VAR)  
  - pattern-not: eval("...")  
  fix: secure_eval($VAR)  
  message: Calling 'eval' with user input  
  languages: [python]  
  severity: WARNING  

```

Given the above is named `rules/detect-eval.yaml`, you can create `rules/detect-eval.py`:



```
from lib import get_user_input, safe_get_user_input, secure_eval  
  
user_input = get_user_input()  
# ruleid: insecure-eval-use  
eval(user_input)  
  
# ok: insecure-eval-use  
eval('print("Hardcoded eval")')  
  
totally_safe_eval = eval  
# todoruleid: insecure-eval-use  
totally_safe_eval(user_input)  
  
# todook: insecure-eval-use  
eval(safe_get_user_input())  

```

Run the tests with the following:



```
semgrep --test rules/  

```

Which will produce the following output:



```
1/1: ✓ All tests passed  
No tests for fixes found.  

```

Semgrep tests automatically avoid failing on lines marked with `# todoruleid` or `# todook`.


Storing rules and test targets in different directories[​](#storing-rules-and-test-targets-in-different-directories "Direct link to Storing rules and test targets in different directories")
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Creating different directories for rules and tests helps users manage
 a growing library of custom rules. To store rules and test targets in 
different directories use the `--config` option.


For example, in the directory with the following structure:



```
$ tree tests  
  
tests  
├── rules  
│   └── python  
│       └── insecure-eval-use.yaml  
└── targets  
    └── python  
        └── insecure-eval-use.py  
  
4 directories, 2 files  

```

Use of the following command:



```
semgrep --test --config tests/rules/ tests/targets/  

```

Produces the same output as in the previous example.


The subdirectory structure of these two directories must be the same for Semgrep to correctly find the associated files.


To test the autofix behavior, add the autofix test file `rules/detect-eval.fixed.py` to represent the expected outcome of applying the fix to the test code:



```
from lib import get_user_input, safe_get_user_input, secure_eval  
  
user_input = get_user_input()  
# ruleid: insecure-eval-use  
secure_eval(user_input)  
  
# ok: insecure-eval-use  
eval('print("Hardcoded eval")')  
  
totally_safe_eval = eval  
# todoruleid: insecure-eval-use  
totally_safe_eval(user_input)  
  
# todook: insecure-eval-use  
secure_eval(safe_get_user_input())  

```

So that the directory structure is printed as the following:



```
$ tree tests  
  
tests  
├── rules  
│   └── python  
│       └── insecure-eval-use.yaml  
└── targets  
    └── python  
        └── insecure-eval-use.py  
        └── insecure-eval-use.fixed.py  
  
4 directories, 2 files  

```

Use of the following command:



```
semgrep --test --config tests/rules/ tests/targets/  

```

Results in the following outcome:



```
1/1: ✓ All tests passed  
1/1: ✓ All fix tests passed  

```

If the fix does not behave as expected, the output prints a line diff.
For example, if we replace `secure_eval` with `safe_eval`, we can see that lines 5 and 15 are not rendered as expected.



```
1/1: ✓ All tests passed  
0/1: 1 fix tests did not pass:  
--------------------------------------------------------------------------------  
	✖ targets/python/detect-eval.fixed.py <> autofix applied to targets/python/detect-eval.py  
  
	---  
	+++  
	@@ -5 +5 @@  
	-safe_eval(user_input)  
	+secure_eval(user_input)  
	@@ -15 +15 @@  
	-safe_eval(safe_get_user_input())  
	+secure_eval(safe_get_user_input())  
  

```

Validating rules[​](#validating-rules "Direct link to Validating rules")
------------------------------------------------------------------------


At Semgrep, Inc., we believe in checking the code we write, and that includes rules.


You can run `semgrep --validate --config [filename]` to 
check the configuration. This command runs a combination of Semgrep 
rules and OCaml checks against your rules to search for issues such as 
duplicate patterns and missing fields. All rules submitted to the 
Semgrep Registry are validated.


The semgrep rules are pulled from `p/semgrep-rule-lints`.


This feature is still experimental and under active development. Your feedback is welcomed!


Enabling autofix in Semgrep Code[​](#enabling-autofix-in-semgrep-code "Direct link to Enabling autofix in Semgrep Code")
------------------------------------------------------------------------------------------------------------------------


To enable autofix for all projects in your Semgrep AppSec Platform organization, follow these steps:


1. In Semgrep AppSec Platform, click **[Settings](https://semgrep.dev/orgs/-/settings)** on the left sidebar.
2. Click **Autofix**  toggle.


---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/testing-rules.md)Last updated on **Jun 12, 2024**[PreviousRule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)[NextPrivate rules](https://semgrep.dev/docs/writing-rules/private-rules)* [Testing autofix](#testing-autofix)
* [Example](#example)
* [Storing rules and test targets in different directories](#storing-rules-and-test-targets-in-different-directories)
* [Validating rules](#validating-rules)
* [Enabling autofix in Semgrep Code](#enabling-autofix-in-semgrep-code)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Testing%20rules%20_%20Semgrep_files/adsct_002.gif)![](Testing%20rules%20_%20Semgrep_files/adsct.gif)









Data\-flow status \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Data-flow%20status%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
		- [Pattern syntax (Experimental)](https://semgrep.dev/docs/writing-rules/experiments/pattern-syntax)
		- [Aliengrep](https://semgrep.dev/docs/writing-rules/experiments/aliengrep)
		- [Displaying propagated value of metavariables](https://semgrep.dev/docs/writing-rules/experiments/display-propagated-metavariable)
		- [Extract mode](https://semgrep.dev/docs/writing-rules/experiments/extract-mode)
		- [Join mode](https://semgrep.dev/docs/writing-rules/experiments/join-mode/overview)
		- [Including multiple focus metavariables using set union semantics](https://semgrep.dev/docs/writing-rules/experiments/multiple-focus-metavariables)
		- [r2c\-internal\-project\-depends\-on](https://semgrep.dev/docs/writing-rules/experiments/r2c-internal-project-depends-on)
		- [Symbolic propagation](https://semgrep.dev/docs/writing-rules/experiments/symbolic-propagation)
		- [Matching captured metavariables with specific types](https://semgrep.dev/docs/writing-rules/experiments/metavariable-type)
		- [Deprecated experiments](https://semgrep.dev/docs/writing-rules/experiments/deprecated-experiments)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
		- [Constant propagation](https://semgrep.dev/docs/writing-rules/data-flow/constant-propagation)
		- [Taint analysis](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode)
		- [Data\-flow status](https://semgrep.dev/docs/writing-rules/data-flow/status)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
* Data\-flow status
* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Data\-flow status
=================


In principle, the data\-flow analysis engine (which provides taint 
tracking, constant propagation, and symbolic propagation) can run on any
 language [supported by Semgrep](https://semgrep.dev/docs/supported-languages). However, the level of support is lower than for the regular Semgrep matching engine.


When Semgrep performs an analysis of the code, it creates an **abstract syntax tree** (AST) which is then translated into an analysis\-friendly **intermediate language** (IL). Subsequently, Semgrep runs mostly language\-agnostic analysis on IL. However, this translation is not fully complete.


cautionThere
 can be features of some languages that Semgrep does not analyze 
correctly while using data\-flow analysis. Consequently, Semgrep does not
 fail even if it finds an unsupported construct. The analysis continues 
while the construct is ignored. This can result in Semgrep not matching 
some code that should be matched (false negatives) or matching a code 
that should not be matched (false positives).


Please, help us to improve and report any issues you encounter by creating an issue on Semgrep [GitHub](https://github.com/semgrep/semgrep/issues/new/choose) page.



---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/data-flow/status.md)Last updated on **Jun 12, 2024**[PreviousTaint analysis](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode)[NextSAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Data-flow%20status%20_%20Semgrep_files/adsct_002.gif)![](Data-flow%20status%20_%20Semgrep_files/adsct.gif)









Constant propagation \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Constant%20propagation%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
		- [Pattern syntax (Experimental)](https://semgrep.dev/docs/writing-rules/experiments/pattern-syntax)
		- [Aliengrep](https://semgrep.dev/docs/writing-rules/experiments/aliengrep)
		- [Displaying propagated value of metavariables](https://semgrep.dev/docs/writing-rules/experiments/display-propagated-metavariable)
		- [Extract mode](https://semgrep.dev/docs/writing-rules/experiments/extract-mode)
		- [Join mode](https://semgrep.dev/docs/writing-rules/experiments/join-mode/overview)
		- [Including multiple focus metavariables using set union semantics](https://semgrep.dev/docs/writing-rules/experiments/multiple-focus-metavariables)
		- [r2c\-internal\-project\-depends\-on](https://semgrep.dev/docs/writing-rules/experiments/r2c-internal-project-depends-on)
		- [Symbolic propagation](https://semgrep.dev/docs/writing-rules/experiments/symbolic-propagation)
		- [Matching captured metavariables with specific types](https://semgrep.dev/docs/writing-rules/experiments/metavariable-type)
		- [Deprecated experiments](https://semgrep.dev/docs/writing-rules/experiments/deprecated-experiments)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
		- [Constant propagation](https://semgrep.dev/docs/writing-rules/data-flow/constant-propagation)
		- [Taint analysis](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode)
		- [Data\-flow status](https://semgrep.dev/docs/writing-rules/data-flow/status)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
* Constant propagation
On this page* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Constant propagation
====================


Semgrep supports intra\-procedural constant propagation. This analysis tracks whether a variable *must*
 carry a constant value at a given point in the program. Semgrep then 
performs constant folding when matching literal patterns. Semgrep can 
track Boolean, numeric, and string constants.


For example:



`metavariable-comparison`[​](#metavariable-comparison "Direct link to metavariable-comparison")
-----------------------------------------------------------------------------------------------


Using constant propagation, the [`metavariable-comparison`](https://semgrep.dev/docs/writing-rules/rule-syntax#metavariable-comparison) operator works with any constant variable, instead of just literals.


For example:



Mutable objects[​](#mutable-objects "Direct link to Mutable objects")
---------------------------------------------------------------------


In general, Semgrep assumes that constant objects are immutable and 
won't be modified by function calls. This may lead to false positives, 
especially in languages where strings are mutable such as C and Ruby.


The only exceptions are method calls whose returning value is 
ignored. In these cases, Semgrep assumes that the method call may be 
mutating the callee object. This helps reducing false positives in Ruby.
 For example:



If constant propagation doesn't seem to work, consider whether the 
constant may be unexpectedly mutable. For example, given the following 
rule designed to taint the `REGEX` class variable:



```
rules:  
  - id: redos-detection  
    message: Potential ReDoS vulnerability detected with $REGEX  
    severity: ERROR  
    languages:  
      - java  
    mode: taint  
    options:  
      symbolic_propagation: true  
    pattern-sources:  
      - patterns:  
          - pattern: $REDOS  
          - metavariable-analysis:  
              analyzer: redos  
              metavariable: $REDOS  
    pattern-sinks:  
      - pattern: Pattern.compile(...)  

```

Semgrep fails to match its use in `Test2` when presented with the following code:



```
import java.util.regex.Pattern;  
  
public String REGEX = "(a+)+$";  
  
public class Test2 {  
    public static void main(String[] args) {  
        Pattern pattern = Pattern.compile(REGEX);  
    }  
}  

```

However, if you change the variable from `public` to `private`, Semgrep does return a match:



```
import java.util.regex.Pattern;  
  
private String REGEX = "(a+)+$";  
  
public class Test2 {  
    public static void main(String[] args) {  
        Pattern pattern = Pattern.compile(REGEX);  
    }  
}  

```

Because `REGEX` is public in the first code snippet, 
Semgrep doesn't propagate its value to other classes on the assumption 
that it could have mutated. However, in the second example, Semgrep 
understands that `REGEX` is private and is only assigned to once. Therefore, Semgrep assumes it to be immutable.


The rule would also work with:



```
...  
public final String REGEX = "(a+)+$";  
...  

```

Disable constant propagation[​](#disable-constant-propagation "Direct link to Disable constant propagation")
------------------------------------------------------------------------------------------------------------


You can disable constant propagation in a per\-rule basis using rule [`options:`](https://semgrep.dev/docs/writing-rules/rule-syntax#options) by setting `constant_propagation: false`.




---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/data-flow/constant-propagation.md)Last updated on **Jun 25, 2024**[PreviousEngine overview](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)[NextTaint analysis](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode)* [`metavariable-comparison`](#metavariable-comparison)
* [Mutable objects](#mutable-objects)
* [Disable constant propagation](#disable-constant-propagation)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Constant%20propagation%20_%20Semgrep_files/adsct.gif)![](Constant%20propagation%20_%20Semgrep_files/adsct_002.gif)









Generic pattern matching \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Generic%20pattern%20matching%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* Generic pattern matching
On this page* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Generic pattern matching
========================


Introduction[​](#introduction "Direct link to Introduction")
------------------------------------------------------------


Semgrep can match generic patterns in languages that it does **not**
 yet support. Use generic pattern matching for languages that do not 
have a parser, configuration files, or other structured data such as 
XML. Generic pattern matching can also be useful in files containing 
multiple languages even if the languages are otherwise supported, such 
as HTML with embedded JavaScript or PHP code. In those cases you can 
also consider [Extract mode (experimental)](https://semgrep.dev/docs/writing-rules/experiments/extract-mode), but generic patterns may be simpler and still effective.


As an example of generic matching, consider this rule:



```
rules:  
  - id: dynamic-proxy-scheme  
    pattern: proxy_pass $$SCHEME:// ...;  
    paths:  
      include:  
        - "*.conf"  
        - "*.vhost"  
        - sites-available/*  
        - sites-enabled/*  
    languages:  
      - generic  
    severity: WARNING  
    message: >-  
      The protocol scheme for this proxy is dynamically determined.  
      This can be dangerous if the scheme is injected by an  
      attacker because it may forcibly alter the connection scheme.  
      Consider hardcoding a scheme for this proxy.  
    metadata:  
      references:  
        - https://github.com/yandex/gixy/blob/master/docs/en/plugins/ssrf.md  
      category: security  
      technology:  
        - nginx  
      confidence: MEDIUM  

```

The above rule [matches](https://semgrep.dev/playground/r/generic.nginx.security.dynamic-proxy-scheme.dynamic-proxy-scheme) this code snippet:



```
server {  
  listen              443 ssl;  
  server_name         www.example.com;  
  keepalive_timeout   70;  
  
  ssl_certificate     www.example.com.crt;  
  ssl_certificate_key www.example.com.key;  
  
  location ~ /proxy/(.*)/(.*)/(.*)$ {  
    # ruleid: dynamic-proxy-scheme  
    proxy_pass $1://$2/$3;  
  }  
  
  location ~* ^/internal-proxy/(?<proxy_proto>https?)/(?<proxy_host>.*?)/(?<proxy_path>.*)$ {  
    internal;  
  
    # ruleid: dynamic-proxy-scheme  
    proxy_pass $proxy_proto://$proxy_host/$proxy_path ;  
    proxy_set_header Host $proxy_host;  
}  
  
  location ~ /proxy/(.*)/(.*)/(.*)$ {  
    # ok: dynamic-proxy-scheme  
    proxy_pass http://$1/$2/$3;  
  }  
  
  location ~ /proxy/(.*)/(.*)/(.*)$ {  
    # ok: dynamic-proxy-scheme  
    proxy_pass https://$1/$2/$3;  
  }  
}  

```

Generic pattern matching has the following properties:


* A document is interpreted as a nested sequence of ASCII words, ASCII punctuation, and other bytes.
* `...` (ellipsis operator) allows skipping non\-matching elements, up to 10 lines down the last match.
* `$X` (metavariable) matches any word.
* `$...X` (ellipsis metavariable) matches a sequence of words, up to 10 lines down the last match.
* Indentation determines primary nesting in the document.
* Common ASCII braces `()`, `[]`, and `{}`
 introduce secondary nesting but only within single lines. Therefore, 
misinterpreted or mismatched braces don't disturb the structure of the 
rest of document.
* The document must be at least as indented as the pattern: any 
indentation specified in the pattern must be honored in the document.


Caveats and limitations of generic mode[​](#caveats-and-limitations-of-generic-mode "Direct link to Caveats and limitations of generic mode")
---------------------------------------------------------------------------------------------------------------------------------------------


Semgrep can reliably understand the syntax of natively [supported languages](https://semgrep.dev/docs/supported-languages). The generic mode is useful for unsupported languages, and consequently brings specific limitations.


cautionThe quality of results in the generic mode can vary depending on the language you use it for.


The generic mode works fine with any human\-readable text, as long as 
it is primarily based on ASCII symbols. Since the generic mode does not 
understand the syntax of the language you are scanning, the quality of 
the result may differ from language to language or even depend on 
specific code. As a consequence, the generic mode works well for some 
languages, but it does not always give consistent results. Generally, 
it's possible or even easy to write code in weird ways that prevent 
generic mode from matching.


**Example**: In XML, one can write `&#x48;&#x65;&#x6C;&#x6C;&#x6F` instead of `Hello`. If a rule pattern in generic mode is `Hello`, Semgrep is unable to match the `&#x48;&#x65;&#x6C;&#x6C;&#x6F`, unlike if it had full XML support.


With respect to Semgrep operators and features:


* metavariable support is limited to capturing a single “word”, which 
is a token of the form \[A\-Za\-z0\-9\_]\+. They can’t capture sequences of 
tokens such as hello, world (in this case there are 3 tokens: `hello`, `,`, and `world`).
* the ellipsis operator is supported and spans at most 10 lines
* pattern operators like either/not/inside are supported
* inline regular expressions for strings (`"=~/word.*/"`) are not supported


Troubleshooting[​](#troubleshooting "Direct link to Troubleshooting")
---------------------------------------------------------------------


### Common pitfall \#1: not enough `...`[​](#common-pitfall-1-not-enough- "Direct link to common-pitfall-1-not-enough-")


Rule of thumb:



> If the pattern commonly matches many lines, use `... ...` (20 lines), or `... ... ...` (30 lines) etc. to make sure to match all the lines.


Here's an innocuous pattern that should match the call to a function `f()`:



```
f(...)  

```

It matches the following code [just fine](https://semgrep.dev/s/9v9R):



```
f(  
  1,  
  2,  
  3,  
  4,  
  5,  
  6,  
  7,  
  8,  
  9  
)  

```

But it will [fail](https://semgrep.dev/s/1z6Q) here because the function arguments span more than 10 lines:



```
f(  
  1,  
  2,  
  3,  
  4,  
  5,  
  6,  
  7,  
  8,  
  9,  
  10  
)  

```

The [solution](https://semgrep.dev/s/9v9R) is to use multiple `...` in the pattern:



```
f(... ...)  

```

### Common pitfall \#2: not enough indentation[​](#common-pitfall-2-not-enough-indentation "Direct link to Common pitfall #2: not enough indentation")


Rule of thumb:



> If the target code is always indented, use indentation in the pattern.


In the following example, we want to match the `system` sections containing a `name` field:



```
# match here  
[system]  
  name = "Debian"  
  
# DON'T match here  
[system]  
  max_threads = 2  
[user]  
  name = "Admin Overlord"  

```

❌ This pattern will [incorrectly](https://semgrep.dev/s/ry1A) catch the `name` field in the `user` section:



```
[system]  
...  
name = ...  

```

✅ This pattern will catch [only](https://semgrep.dev/s/bXAr) the `name` field in the `system` section:



```
[system]  
  ...  
  name = ...  

```

### Handling line\-based input[​](#handling-line-based-input "Direct link to Handling line-based input")


This section explains how to use Semgrep's generic mode to match
single lines of code using an ellipsis metavariable. Many simple
configuration formats are collections of key and value pairs delimited
by newlines. For example, to extract the `password` value from the
following made\-up input:



```
username = bob  
password = p@$$w0rd  
server = example.com  

```

Unfortunately, the following pattern does not match the whole line. 
In generic mode, metavariables only capture a single word (alphanumeric 
sequence):



```
password = $PASSWORD  

```

This pattern matches the input file but does not assign the value `p` to `$PASSWORD` instead of the full value `p@$$w0rd`.


To match an arbitrary sequence of items and capture their value in the example:


1. Use a named ellipsis, by changing the pattern to the following:



```
password = $...PASSWORD  

```

This still leads Semgrep to capture too much information. The value assigned to `$...PASSWORD` are now `p@$$w0rd` and  

`server = example.com`. In generic mode, an ellipsis extends 
until the end of the current block or up to 10 lines below, whichever 
comes first. To prevent this behavior, continue with the next step.
2. In the Semgrep rule, specify the following key:



```
generic_ellipsis_max_span: 0  

```

This option forces the ellipsis operator to match patterns within a single line.
Example of the [resulting rule](https://semgrep.dev/playground/s/KPzn):



```
id: password-in-config-file  
pattern: |  
  password = $...PASSWORD  
options:  
  # prevent ellipses from matching multiple lines  
  generic_ellipsis_max_span: 0  
message: |  
  password found in config file: $...PASSWORD  
languages:  
  - generic  
severity: WARNING  

```


### Ignoring comments[​](#ignoring-comments "Direct link to Ignoring comments")


By default, the generic mode does **not** know about comments or code
that can be ignored. In the following example, we are
scanning for CSS code that sets the text color to blue. The target code
is the following:



```
color: /* my fave color */ blue;  

```

Use the [`options.generic_comment_style`](https://semgrep.dev/docs/writing-rules/rule-syntax#options)
to ignore C\-style comments as it is the case in our example.
Our simple Semgrep rule is:



```
id: css-blue-is-ugly  
pattern: |  
  color: blue  
options:  
  # ignore comments of the form /* ... */  
  generic_comment_style: c  
message: |  
  Blue is ugly.  
languages:  
  - generic  
severity: WARNING  

```

Command line example[​](#command-line-example "Direct link to Command line example")
------------------------------------------------------------------------------------


Sample pattern: `exec(...)`


Sample target file `exec.txt` contains:



```
import exec as safe_function  
safe_function(user_input)  
  
exec("ls")  
  
exec(some_var)  
  
some_exec(foo)  
  
exec (foo)  
  
exec (  
    bar  
)  
  
# exec(foo)  
  
print("exec(bar)")  

```

Output:



```
$ semgrep -l generic -e 'exec(...)` exec.text  
7:exec("ls")  
--------------------------------------------------------------------------------  
11:exec(some_var)  
--------------------------------------------------------------------------------  
19:exec (foo)  
--------------------------------------------------------------------------------  
23:exec (  
24:128  
25:    bar  
26:129  
27:)  
--------------------------------------------------------------------------------  
31:# exec(foo)  
--------------------------------------------------------------------------------  
35:print("exec(bar)")  
ran 1 rules on 1 files: 6 findings  

```

Semgrep Registry rules for generic pattern matching[​](#semgrep-registry-rules-for-generic-pattern-matching "Direct link to Semgrep Registry rules for generic pattern matching")
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


You can peruse [existing generic rules](https://semgrep.dev/r?lang=generic&sev=ERROR,WARNING,INFO&tag=dgryski.semgrep-go,hazanasec.semgrep-rules,ajinabraham.njsscan,best-practice,security,java-spring,go-stdlib,ruby-stdlib,java-stdlib,js-node,nodejsscan,owasp,dlint,react,performance,compatibility,portability,correctness,maintainability,secuirty,mongodb,experimental,caching,robots-denied,missing-noreferrer,missing-noopener) in the Semgrep registry. In general, short patterns on structured data will perform the best.


Cheat sheet[​](#cheat-sheet "Direct link to Cheat sheet")
---------------------------------------------------------


Some examples of what will and will not match on the `generic` tab of the Semgrep cheat sheet below:



  

Hidden bonus[​](#hidden-bonus "Direct link to Hidden bonus")
------------------------------------------------------------


In the Semgrep code the generic pattern matching implementation is called **spacegrep** because it tokenizes based on whitespace (and because it sounds cool 😎).



---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/generic-pattern-matching.md)Last updated on **Jun 12, 2024**[PreviousAutofix](https://semgrep.dev/docs/writing-rules/autofix)[NextMetavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)* [Introduction](#introduction)
* [Caveats and limitations of generic mode](#caveats-and-limitations-of-generic-mode)
* [Troubleshooting](#troubleshooting)
	+ [Common pitfall \#1: not enough `...`](#common-pitfall-1-not-enough-)
	+ [Common pitfall \#2: not enough indentation](#common-pitfall-2-not-enough-indentation)
	+ [Handling line\-based input](#handling-line-based-input)
	+ [Ignoring comments](#ignoring-comments)
* [Command line example](#command-line-example)
* [Semgrep Registry rules for generic pattern matching](#semgrep-registry-rules-for-generic-pattern-matching)
* [Cheat sheet](#cheat-sheet)
* [Hidden bonus](#hidden-bonus)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Generic%20pattern%20matching%20_%20Semgrep_files/adsct_002.gif)![](Generic%20pattern%20matching%20_%20Semgrep_files/adsct.gif)









Rule syntax \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Rule%20syntax%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* Rule syntax
On this page* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Rule syntax
===========


tipGetting started with rule writing? Try the [Semgrep Tutorial](https://semgrep.dev/learn) 🎓


This document describes the YAML rule syntax of Semgrep.


Schema[​](#schema "Direct link to Schema")
------------------------------------------


### Required[​](#required "Direct link to Required")


All required fields must be present at the top\-level of a rule, immediately under the `rules` key.




| Field | Type | Description |
| --- | --- | --- |
| `id` | `string` | Unique, descriptive identifier, for example: `no-unused-variable` |
| `message` | `string` | Message that includes why Semgrep matched this pattern and how to remediate it. See also [Rule messages](https://semgrep.dev/docs/contributing/contributing-to-semgrep-rules-repository#rule-messages). |
| `severity` | `string` | One of the following values: `INFO` (Low severity), `WARNING` (Medium severity), or `ERROR` (High severity). The `severity`  key specifies how critical are the issues that a rule potentially  detects. Note: Semgrep Supply Chain differs, as its rules use CVE  assignments for severity. For more information, see [Filters](https://semgrep.dev/docs/semgrep-supply-chain/triage-and-remediation#filters) section in Semgrep Supply Chain documentation. |
| `languages` | `array` | See [language extensions and tags](https://semgrep.dev/docs/writing-rules/rule-syntax#language-extensions-and-languages-key-values) |
| `pattern`*\** | `string` | Find code matching this expression |
| `patterns`*\** | `array` | Logical AND of multiple patterns |
| `pattern-either`*\** | `array` | Logical OR of multiple patterns |
| `pattern-regex`*\** | `string` | Find code matching this [PCRE2](https://www.pcre.org/current/doc/html/pcre2pattern.html)\-compatible pattern in multiline mode |


infoOnly one of the following is required: `pattern`, `patterns`, `pattern-either`, `pattern-regex`


#### Language extensions and languages key values[​](#language-extensions-and-languages-key-values "Direct link to Language extensions and languages key values")


The following table includes languages supported by Semgrep, accepted
 file extensions for test files that accompany rules, and valid values 
that Semgrep rules require in the `languages` key.




| Language | Extensions | `languages` key values |
| --- | --- | --- |
| Apex (only in Semgrep Pro Engine) | `.cls` | `apex` |
| Bash | `.bash`, `.sh` | `bash`, `sh` |
| C | `.c` | `c` |
| Cairo | `.cairo` | `cairo` |
| Clojure | `.clj`, `.cljs`, `.cljc`, `.edn` | `clojure` |
| C\+\+ | `.cc`, `.cpp` | `cpp`, `c++` |
| C\# | `.cs` | `csharp`, `c#` |
| Dart | `.dart` | `dart` |
| Dockerfile | `.dockerfile`, `.Dockerfile` | `dockerfile`, `docker` |
| Elixir | `.ex`, `.exs` | `ex`, `elixir` |
| Generic |  | `generic` |
| Go | `.go` | `go`, `golang` |
| HTML | `.htm`, `.html` | `html` |
| Java | `.java` | `java` |
| JavaScript | `.js`, `.jsx` | `js`, `javascript` |
| JSON | `.json`, `.ipynb` | `json` |
| Jsonnet | `.jsonnet`, `.libsonnet` | `jsonnet` |
| JSX | `.js`, `.jsx` | `js`, `javascript` |
| Julia | `.jl` | `julia` |
| Kotlin | `.kt`, `.kts`, `.ktm` | `kt`, `kotlin` |
| Lisp | `.lisp`, `.cl`, `.el` | `lisp` |
| Lua | `.lua` | `lua` |
| OCaml | `.ml`, `.mli` | `ocaml` |
| PHP | `.php`, `.tpl` | `php` |
| Python | `.py`, `.pyi` | `python`, `python2`, `python3`, `py` |
| R | `.r`, `.R` | `r` |
| Ruby | `.rb` | `ruby` |
| Rust | `.rs` | `rust` |
| Scala | `.scala` | `scala` |
| Scheme | `.scm`, `.ss` | `scheme` |
| Solidity | `.sol` | `solidity`, `sol` |
| Swift | `.swift` | `swift` |
| Terraform | `.tf`, `.hcl` | `tf`, `hcl`, `terraform` |
| TypeScript | `.ts`, `.tsx` | `ts`, `typescript` |
| YAML | `.yml`, `.yaml` | `yaml` |
| XML | `.xml` | `xml` |


infoTo see the maturity level of each supported language, see the following sections in [Supported languages](https://semgrep.dev/docs/supported-languages) document:

* [Semgrep OSS Engine](https://semgrep.dev/docs/supported-languages#semgrep-oss-language-support)
* [Semgrep Pro Engine](https://semgrep.dev/docs/supported-languages#semgrep-code-language-support)

### Optional[​](#optional "Direct link to Optional")




| Field | Type | Description |
| --- | --- | --- |
| [`options`](#options) | `object` | Options object to enable/disable certain matching features |
| [`fix`](#fix) | `object` | Simple search\-and\-replace autofix functionality |
| [`metadata`](#metadata) | `object` | Arbitrary user\-provided data; attach data to rules without affecting Semgrep behavior |
| [`min-version`](#min-version-and-max-version) | `string` | Minimum Semgrep version compatible with this rule |
| [`max-version`](#min-version-and-max-version) | `string` | Maximum Semgrep version compatible with this rule |
| [`paths`](#paths) | `object` | Paths to include or exclude when running this rule |


The below optional fields must reside underneath a `patterns` or `pattern-either` field.




| Field | Type | Description |
| --- | --- | --- |
| [`pattern-inside`](#pattern-inside) | `string` | Keep findings that lie inside this pattern |


The below optional fields must reside underneath a `patterns` field.




| Field | Type | Description |
| --- | --- | --- |
| [`metavariable-regex`](#metavariable-regex) | `map` | Search metavariables for [Python `re`](https://docs.python.org/3/library/re.html#re.match) compatible expressions; regex matching is **unanchored** |
| [`metavariable-pattern`](#metavariable-pattern) | `map` | Matches metavariables with a pattern formula |
| [`metavariable-comparison`](#metavariable-comparison) | `map` | Compare metavariables against basic [Python expressions](https://docs.python.org/3/reference/expressions.html#comparisons) |
| [`pattern-not`](#pattern-not) | `string` | Logical NOT \- remove findings matching this expression |
| [`pattern-not-inside`](#pattern-not-inside) | `string` | Keep findings that do not lie inside this pattern |
| [`pattern-not-regex`](#pattern-not-regex) | `string` | Filter results using a [PCRE2](https://www.pcre.org/current/doc/html/pcre2pattern.html)\-compatible pattern in multiline mode |


Operators[​](#operators "Direct link to Operators")
---------------------------------------------------


### `pattern`[​](#pattern "Direct link to pattern")


The `pattern` operator looks for code matching its expression. This can be basic expressions like `$X == $X` or unwanted function calls like `hashlib.md5(...)`.



```
rules:  
  - id: md5-usage  
    languages:  
      - python  
    message: Found md5 usage  
    pattern: hashlib.md5(...)  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
import hashlib  
# ruleid: md5-usage  
digest = hashlib.md5(b"test")  
# ok: md5-usage  
digest = hashlib.sha256(b"test")  

```

### `patterns`[​](#patterns "Direct link to patterns")


The `patterns` operator performs a logical AND operation 
on one or more child patterns. This is useful for chaining multiple 
patterns together that all must be true.



```
rules:  
  - id: unverified-db-query  
    patterns:  
      - pattern: db_query(...)  
      - pattern-not: db_query(..., verify=True, ...)  
    message: Found unverified db query  
    severity: ERROR  
    languages:  
      - python  

```

The pattern immediately above matches the following:



```
# ruleid: unverified-db-query  
db_query("SELECT * FROM ...")  
# ok: unverified-db-query  
db_query("SELECT * FROM ...", verify=True, env="prod")  

```

#### `patterns` operator evaluation strategy[​](#patterns-operator-evaluation-strategy "Direct link to patterns-operator-evaluation-strategy")


Note that the order in which the child patterns are declared in a `patterns` operator has no effect on the final result. A `patterns` operator is always evaluated in the same way:


1. Semgrep evaluates all *positive* patterns, that is [`pattern-inside`](#pattern-inside)s, [`pattern`](#pattern)s, [`pattern-regex`](#pattern-regex)es, and [`pattern-either`](#pattern-either)s.
 Each range matched by each one of these patterns is intersected with 
the ranges matched by the other operators. The result is a set of *positive* ranges. The positive ranges carry *metavariable bindings*. For example, in one range `$X` can be bound to the function call `foo()`, and in another range `$X` can be bound to the expression `a + b`.
2. Semgrep evaluates all *negative* patterns, that is [`pattern-not-inside`](#pattern-not-inside)s, [`pattern-not`](#pattern-not)s, and [`pattern-not-regex`](#pattern-not-regex)es. This gives a set of *negative ranges*
 which are used to filter the positive ranges. This results in a strict 
subset of the positive ranges computed in the previous step.
3. Semgrep evaluates all *conditionals*, that is [`metavariable-regex`](#metavariable-regex)es, [`metavariable-pattern`](#metavariable-pattern)s and [`metavariable-comparison`](#metavariable-comparison)s.
 These conditional operators can only examine the metavariables bound in
 the positive ranges in step 1, that passed through the filter of 
negative patterns in step 2\. Note that metavariables bound by negative 
patterns are *not* available here.
4. Semgrep applies all [`focus-metavariable`](#focus-metavariable)s,
 by computing the intersection of each positive range with the range of 
the metavariable on which we want to focus. Again, the only 
metavariables available to focus on are those bound by positive 
patterns.


### `pattern-either`[​](#pattern-either "Direct link to pattern-either")


The `pattern-either` operator performs a logical OR 
operation on one or more child patterns. This is useful for chaining 
multiple patterns together where any may be true.



```
rules:  
  - id: insecure-crypto-usage  
    pattern-either:  
      - pattern: hashlib.sha1(...)  
      - pattern: hashlib.md5(...)  
    message: Found insecure crypto usage  
    languages:  
      - python  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
import hashlib  
# ruleid: insecure-crypto-usage  
digest = hashlib.md5(b"test")  
# ruleid: insecure-crypto-usage  
digest = hashlib.sha1(b"test")  
# ok: insecure-crypto-usage  
digest = hashlib.sha256(b"test")  

```

This rule looks for usage of the Python standard library functions `hashlib.md5` or `hashlib.sha1`. Depending on their usage, these hashing functions are [considered insecure](https://shattered.io/).


### `pattern-regex`[​](#pattern-regex "Direct link to pattern-regex")


The `pattern-regex` operator searches files for substrings matching the given [PCRE2](https://www.pcre.org/current/doc/html/pcre2pattern.html)
 pattern. This is useful for migrating existing regular expression code 
search functionality to Semgrep. Perl\-Compatible Regular Expressions 
(PCRE) is a full\-featured regex library that is widely compatible with 
Perl, but also with the respective regex libraries of Python, 
JavaScript, Go, Ruby, and Java. Patterns are compiled in multiline mode,
 for example `^` and `$` matches at the beginning and end of lines respectively in addition to the beginning and end of input.


cautionPCRE2 supports [some Unicode character properties, but not some Perl properties](https://www.pcre.org/current/doc/html/pcre2pattern.html#uniextseq). For example, `\p{Egyptian_Hieroglyphs}` is supported but `\p{InMusicalSymbols}` isn't.


#### Example: `pattern-regex` combined with other pattern operators[​](#example-pattern-regex-combined-with-other-pattern-operators "Direct link to example-pattern-regex-combined-with-other-pattern-operators")



```
rules:  
  - id: boto-client-ip  
    patterns:  
      - pattern-inside: boto3.client(host="...")  
      - pattern-regex: \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}  
    message: boto client using IP address  
    languages:  
      - python  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
import boto3  
# ruleid: boto-client-ip  
client = boto3.client(host="192.168.1.200")  
# ok: boto-client-ip  
client = boto3.client(host="dev.internal.example.com")  

```

#### Example: `pattern-regex` used as a standalone, top\-level operator[​](#example-pattern-regex-used-as-a-standalone-top-level-operator "Direct link to example-pattern-regex-used-as-a-standalone-top-level-operator")



```
rules:  
  - id: legacy-eval-search  
    pattern-regex: eval\(  
    message: Insecure code execution  
    languages:  
      - javascript  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
# ruleid: legacy-eval-search  
eval('var a = 5')  

```

infoSingle (`'`) and double (`"`) quotes [behave differently](https://docs.octoprint.org/en/master/configuration/yaml.html#scalars) in YAML syntax. Single quotes are typically preferred when using backslashes (`\`) with `pattern-regex`.


Note that you may bind a section of a regular expression to a metavariable, by using [named capturing groups](https://www.regular-expressions.info/named.html). In
this case, the name of the capturing group must be a valid metavariable name.



```
rules:  
  - id: my_pattern_id-copy  
    patterns:  
      - pattern-regex: a(?P<FIRST>.*)b(?P<SECOND>.*)  
    message: Semgrep found a match, with $FIRST and $SECOND  
    languages:  
      - regex  
    severity: WARNING  

```

The pattern immediately above matches the following:



```
acbd  

```

### `pattern-not-regex`[​](#pattern-not-regex "Direct link to pattern-not-regex")


The `pattern-not-regex` operator filters results using a [PCRE2](https://www.pcre.org/current/doc/html/pcre2pattern.html)
 regular expression in multiline mode. This is most useful when combined
 with regular\-expression only rules, providing an easy way to filter 
findings without having to use negative lookaheads. `pattern-not-regex` works with regular `pattern` clauses, too.


The syntax for this operator is the same as `pattern-regex`.


This operator filters findings that have *any overlap* with the supplied regular expression. For example, if you use `pattern-regex` to detect `Foo==1.1.1` and it also detects `Foo-Bar==3.0.8` and `Bar-Foo==3.0.8`, you can use `pattern-not-regex` to filter the unwanted findings.



```
rules:  
  - id: detect-only-foo-package  
    languages:  
      - regex  
    message: Found foo package  
    patterns:  
      - pattern-regex: foo  
      - pattern-not-regex: foo-  
      - pattern-not-regex: -foo  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
# ruleid: detect-only-foo-package  
foo==1.1.1  
# ok: detect-only-foo-package  
foo-bar==3.0.8  
# ok: detect-only-foo-package  
bar-foo==3.0.8  

```

### `focus-metavariable`[​](#focus-metavariable "Direct link to focus-metavariable")


The `focus-metavariable` operator puts the focus, or *zooms in*,
 on the code region matched by a single metavariable or a list of 
metavariables. For example, to find all functions arguments annotated 
with the type `bad` you may write the following pattern:



```
pattern: |  
  def $FUNC(..., $ARG : bad, ...):  
    ...  

```

This works but it matches the entire function definition. Sometimes, 
this is not desirable. If the definition spans hundreds of lines they 
are all matched. In particular, if you are using [Semgrep AppSec Platform](https://semgrep.dev/login)
 and you have triaged a finding generated by this pattern, the same 
finding shows up again as new if you make any change to the definition 
of the function!


To specify that you are only interested in the code matched by a particular metavariable, in our example `$ARG`, use `focus-metavariable`.



```
rules:  
  - id: find-bad-args  
    patterns:  
      - pattern: |  
          def $FUNC(..., $ARG : bad, ...):  
            ...  
      - focus-metavariable: $ARG  
    message: |  
      `$ARG' has a "bad" type!  
    languages:  
      - python  
    severity: WARNING  

```

The pattern immediately above matches the following:



```
def f(x : bad):  
    return x  

```

Note that `focus-metavariable: $ARG` is not the same as `pattern: $ARG`! Using `pattern: $ARG` finds all the uses of the parameter `x` which is not what we want! (Note that `pattern: $ARG` does not match the formal parameter declaration, because in this context `$ARG` only matches expressions.)



```
rules:  
  - id: find-bad-args  
    patterns:  
      - pattern: |  
          def $FUNC(..., $ARG : bad, ...):  
            ...  
      - pattern: $ARG  
    message: |  
      `$ARG' has a "bad" type!  
    languages:  
      - python  
    severity: WARNING  

```

The pattern immediately above matches the following:



```
def f(x : bad):  
    return x  

```

In short, `focus-metavariable: $X` is not a pattern in itself, it does not perform any matching, it only focuses the matching on the code already bound to `$X` by other patterns. Whereas `pattern: $X` matches `$X` against your code (and in this context, `$X` only matches expressions)!


#### Including multiple focus metavariables using set intersection semantics[​](#including-multiple-focus-metavariables-using-set-intersection-semantics "Direct link to Including multiple focus metavariables using set intersection semantics")


Include more `focus-metavariable` keys with different metavariables under the `pattern` to match results **only** for the overlapping region of all the focused code:



```
    patterns:  
      - pattern: foo($X, ..., $Y)  
      - focus-metavariable:  
        - $X  
        - $Y  

```


```
rules:  
  - id: intersect-focus-metavariable  
    patterns:  
      - pattern-inside: foo($X, ...)  
      - focus-metavariable: $X  
      - pattern: $Y + ...  
      - focus-metavariable: $Y  
      - pattern: "1"  
    message: Like set intersection, only the overlapping region is highilighted  
    languages:  
      - python  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
# ruleid: intersect-focus-metavariable  
foo (  
    1  
    +  
    2,  
    1  
)  
  
# OK: test  
foo (2+ 1, 1)  

```

infoTo
 make a list of multiple focus metavariables using set union semantics 
that matches the metavariables regardless of their position in code, see
 [Including multiple focus metavariables using set union semantics](https://semgrep.dev/docs/writing-rules/experiments/multiple-focus-metavariables) documentation.


### `metavariable-regex`[​](#metavariable-regex "Direct link to metavariable-regex")


The `metavariable-regex` operator searches metavariables for a [PCRE2](https://www.pcre.org/current/doc/html/pcre2pattern.html) regular expression. This is useful for filtering results based on a [metavariable’s](https://semgrep.dev/docs/writing-rules/pattern-syntax#metavariables) value. It requires the `metavariable` and `regex` keys and can be combined with other pattern operators.



```
rules:  
  - id: insecure-methods  
    patterns:  
      - pattern: module.$METHOD(...)  
      - metavariable-regex:  
          metavariable: $METHOD  
          regex: (insecure)  
    message: module using insecure method call  
    languages:  
      - python  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
# ruleid: insecure-methods  
module.insecure1("test")  
# ruleid: insecure-methods  
module.insecure2("test")  
# ruleid: insecure-methods  
module.insecure3("test")  
# ok: insecure-methods  
module.secure("test")  

```

Regex matching is **unanchored**. For anchored matching, use `\A` for start\-of\-string anchoring and `\Z` for end\-of\-string anchoring. The next example, using the same expression as above but anchored, finds no matches:



```
rules:  
  - id: insecure-methods  
    patterns:  
      - pattern: module.$METHOD(...)  
      - metavariable-regex:  
          metavariable: $METHOD  
          regex: (^insecure$)  
    message: module using insecure method call  
    languages:  
      - python  
    severity: ERROR  

```

infoInclude quotes in your regular expression when using `metavariable-regex` to search string literals. For more details, see [include\-quotes](https://semgrep.dev/playground/s/EbDB) code snippet. [String matching](https://semgrep.dev/docs/writing-rules/pattern-syntax#string-matching) functionality can also be used to search string literals.


### `metavariable-pattern`[​](#metavariable-pattern "Direct link to metavariable-pattern")


The `metavariable-pattern` operator matches metavariables with a pattern formula. This is useful for filtering results based on a [metavariable’s](https://semgrep.dev/docs/writing-rules/pattern-syntax#metavariables) value. It requires the `metavariable` key, and exactly one key of `pattern`, `patterns`, `pattern-either`, or `pattern-regex`. This operator can be nested as well as combined with other operators.


For example, the `metavariable-pattern` can be used to filter out matches that do **not** match certain criteria:



```
rules:  
  - id: disallow-old-tls-versions2  
    languages:  
      - javascript  
    message: Match found  
    patterns:  
      - pattern: |  
          $CONST = require('crypto');  
          ...  
          $OPTIONS = $OPTS;  
          ...  
          https.createServer($OPTIONS, ...);  
      - metavariable-pattern:  
          metavariable: $OPTS  
          patterns:  
            - pattern-not: >  
                {secureOptions: $CONST.SSL_OP_NO_SSLv2 | $CONST.SSL_OP_NO_SSLv3  
                | $CONST.SSL_OP_NO_TLSv1}  
    severity: WARNING  

```

The pattern immediately above matches the following:



```
function bad() {  
    // ruleid:disallow-old-tls-versions2  
    var constants = require('crypto');  
    var sslOptions = {  
    key: fs.readFileSync('/etc/ssl/private/private.key'),  
    secureProtocol: 'SSLv23_server_method',  
    secureOptions: constants.SSL_OP_NO_SSLv2 | constants.SSL_OP_NO_SSLv3  
    };  
    https.createServer(sslOptions);  
}  

```

infoIn this case it is possible to start a `patterns` AND operation with a `pattern-not`, because there is an implicit `pattern: ...` that matches the content of the metavariable.


The `metavariable-pattern` is also useful in combination with `pattern-either`:



```
rules:  
  - id: open-redirect  
    languages:  
      - python  
    message: Match found  
    patterns:  
      - pattern-inside: |  
          def $FUNC(...):  
            ...  
            return django.http.HttpResponseRedirect(..., $DATA, ...)  
      - metavariable-pattern:  
          metavariable: $DATA  
          patterns:  
            - pattern-either:  
                - pattern: $REQUEST  
                - pattern: $STR.format(..., $REQUEST, ...)  
                - pattern: $STR % $REQUEST  
                - pattern: $STR + $REQUEST  
                - pattern: f"...{$REQUEST}..."  
            - metavariable-pattern:  
                metavariable: $REQUEST  
                patterns:  
                  - pattern-either:  
                      - pattern: request.$W  
                      - pattern: request.$W.get(...)  
                      - pattern: request.$W(...)  
                      - pattern: request.$W[...]  
                  - metavariable-regex:  
                      metavariable: $W  
                      regex: (?!get_full_path)  
    severity: WARNING  

```

The pattern immediately above matches the following:



```
from django.http import HttpResponseRedirect  
def unsafe(request):  
    # ruleid:open-redirect  
    return HttpResponseRedirect(request.POST.get("url"))  

```

tipIt is possible to nest `metavariable-pattern` inside `metavariable-pattern`!


infoThe
 metavariable should be bound to an expression, a statement, or a list 
of statements, for this test to be meaningful. A metavariable bound to a
 list of function arguments, a type, or a pattern, always evaluate to 
false.


#### `metavariable-pattern` with nested language[​](#metavariable-pattern-with-nested-language "Direct link to metavariable-pattern-with-nested-language")


If the metavariable's content is a string, then it is possible to use `metavariable-pattern` to match this string as code by specifying the target language via the `language` key. See the following examples of `metavariable-pattern`:


Examples of `metavariable-pattern`* Match JavaScript code inside HTML in the following [Semgrep Playground](https://semgrep.dev/s/z95k) example.
* Filter regex matches in the following [Semgrep Playground](https://semgrep.dev/s/pkNk) example.

#### Example: Match JavaScript code inside HTML[​](#example-match-javascript-code-inside-html "Direct link to Example: Match JavaScript code inside HTML")



```
rules:  
  - id: test  
    languages:  
      - generic  
    message: javascript inside html working!  
    patterns:  
      - pattern: |  
          <script ...>$...JS</script>  
      - metavariable-pattern:  
          language: javascript  
          metavariable: $...JS  
          patterns:  
            - pattern: |  
                console.log(...)  
    severity: WARNING  
  

```

The pattern immediately above matches the following:



```
<!-- ruleid:test -->  
<script>  
console.log("hello")  
</script>  

```

#### Example: Filter regex matches[​](#example-filter-regex-matches "Direct link to Example: Filter regex matches")



```
rules:  
  - id: test  
    languages:  
      - generic  
    message: "Google dependency: $1 $2"  
    patterns:  
      - pattern-regex: gem "(.*)", "(.*)"  
      - metavariable-pattern:  
          metavariable: $1  
          language: generic  
          patterns:  
            - pattern: google  
    severity: INFO  

```

The pattern immediately above matches the following:



```
source "https://rubygems.org"  
  
#OK:test  
gem "functions_framework", "~> 0.7"  
#ruleid:test  
gem "google-cloud-storage", "~> 1.29"  

```

### `metavariable-comparison`[​](#metavariable-comparison "Direct link to metavariable-comparison")


The `metavariable-comparison` operator compares metavariables against a basic [Python comparison](https://docs.python.org/3/reference/expressions.html#comparisons) expression. This is useful for filtering results based on a [metavariable's](https://semgrep.dev/docs/writing-rules/pattern-syntax#metavariables) numeric value.


The `metavariable-comparison` operator is a mapping which requires the `metavariable` and `comparison` keys. It can be combined with other pattern operators in the following [Semgrep Playground](https://semgrep.dev/s/GWv6) example.


This matches code such as `set_port(80)` or `set_port(443)`, but not `set_port(8080)`.


Comparison expressions support simple arithmetic as well as composition with [Boolean operators](https://docs.python.org/3/reference/expressions.html#boolean-operations)
 to allow for more complex matching. This is particularly useful for 
checking that metavariables are divisible by particular values, such as 
enforcing that a particular value is even or odd.



```
rules:  
  - id: superuser-port  
    languages:  
      - python  
    message: module setting superuser port  
    patterns:  
      - pattern: set_port($ARG)  
      - metavariable-comparison:  
          comparison: $ARG < 1024 and $ARG % 2 == 0  
          metavariable: $ARG  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
# ok: superuser-port  
set_port(443)  
# ruleid: superuser-port  
set_port(80)  
# ok: superuser-port  
set_port(8080)  

```

Building on the previous example, this still matches code such as `set_port(80)` but it no longer matches `set_port(443)` or `set_port(8080)`.


The `comparison` key accepts Python expression using:


* Boolean, string, integer, and float literals.
* Boolean operators `not`, `or`, and `and`.
* Arithmetic operators `+`, `-`, `*`, `/`, and `%`.
* Comparison operators `==`, `!=`, `<`, `<=`, `>`, and `>=`.
* Function `int()` to convert strings into integers.
* Function `str()` to convert numbers into strings.
* Function `today()` that gets today's date as a float representing epoch time.
* Function `strptime()` that converts strings in the format `"yyyy-mm-dd"` to a float representing the date in epoch time.
* Lists, together with the `in`, and `not in` infix operators.
* Strings, together with the `in` and `not in` infix operators, for substring containment.
* Function `re.match()` to match a regular expression (without the optional `flags` argument).


You can use Semgrep metavariables such as `$MVAR`, which Semgrep evaluates as follows:


* If `$MVAR` binds to a literal, then that literal is the value assigned to `$MVAR`.
* If `$MVAR` binds to a code variable that is a constant, 
and constant propagation is enabled (as it is by default), then that 
constant is the value assigned to `$MVAR`.
* Otherwise the code bound to the `$MVAR` is kept unevaluated, and its string representation can be obtained using the `str()` function, as in `str($MVAR)`. For example, if `$MVAR` binds to the code variable `x`, `str($MVAR)` evaluates to the string literal `"x"`.


#### Legacy `metavariable-comparison` keys[​](#legacy-metavariable-comparison-keys "Direct link to legacy-metavariable-comparison-keys")


infoYou can avoid the use of the legacy keys described below (`base: int` and `strip: bool`) by using the `int()` function, as in `int($ARG) > 0o600` or `int($ARG) > 2147483647`.


The `metavariable-comparison` operator also takes optional `base: int` and `strip: bool`
 keys. These keys set the integer base the metavariable value should be 
interpreted as and remove quotes from the metavariable value, 
respectively.



```
rules:  
  - id: excessive-permissions  
    languages:  
      - python  
    message: module setting excessive permissions  
    patterns:  
      - pattern: set_permissions($ARG)  
      - metavariable-comparison:  
          comparison: $ARG > 0o600  
          metavariable: $ARG  
          base: 8  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
# ruleid: excessive-permissions  
set_permissions(0o700)  
# ok: excessive-permissions  
set_permissions(0o400)  

```

This interprets metavariable values found in code as octal. As a result, Semgrep detects `0700`, but it does **not** detect `0400`.



```
rules:  
  - id: int-overflow  
    languages:  
      - python  
    message: Potential integer overflow  
    patterns:  
      - pattern: int($ARG)  
      - metavariable-comparison:  
          strip: true  
          comparison: $ARG > 2147483647  
          metavariable: $ARG  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
# ruleid: int-overflow  
int("2147483648")  
# ok: int-overflow  
int("2147483646")  

```

This removes quotes (`'`, `"`, and ```) from both ends of the metavariable content. As a result, Semgrep detects `"2147483648"`, but it does **not** detect `"2147483646"`. This is useful when you expect strings to contain integer or float data.


### `pattern-not`[​](#pattern-not "Direct link to pattern-not")


The `pattern-not` operator is the opposite of the `pattern` operator. It finds code that does not match its expression. This is useful for eliminating common false positives.



```
rules:  
  - id: unverified-db-query  
    patterns:  
      - pattern: db_query(...)  
      - pattern-not: db_query(..., verify=True, ...)  
    message: Found unverified db query  
    severity: ERROR  
    languages:  
      - python  

```

The pattern immediately above matches the following:



```
# ruleid: unverified-db-query  
db_query("SELECT * FROM ...")  
# ok: unverified-db-query  
db_query("SELECT * FROM ...", verify=True, env="prod")  

```

### `pattern-inside`[​](#pattern-inside "Direct link to pattern-inside")


The `pattern-inside` operator keeps matched findings that 
reside within its expression. This is useful for finding code inside 
other pieces of code like functions or if blocks.



```
rules:  
  - id: return-in-init  
    patterns:  
      - pattern: return ...  
      - pattern-inside: |  
          class $CLASS:  
            ...  
      - pattern-inside: |  
          def __init__(...):  
              ...  
    message: return should never appear inside a class __init__ function  
    languages:  
      - python  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
class A:  
    def __init__(self):  
        # ruleid: return-in-init  
        return None  
  
class B:  
    def __init__(self):  
        # ok: return-in-init  
        self.inited = True  
  
def foo():  
    # ok: return-in-init  
    return 5  

```

### `pattern-not-inside`[​](#pattern-not-inside "Direct link to pattern-not-inside")


The `pattern-not-inside` operator keeps matched findings that do not reside within its expression. It is the opposite of `pattern-inside`.
 This is useful for finding code that’s missing a corresponding cleanup 
action like disconnect, close, or shutdown. It’s also useful for finding
 problematic code that isn't inside code that mitigates the issue.



```
rules:  
  - id: open-never-closed  
    patterns:  
      - pattern: $F = open(...)  
      - pattern-not-inside: |  
          $F = open(...)  
          ...  
          $F.close()  
    message: file object opened without corresponding close  
    languages:  
      - python  
    severity: ERROR  

```

The pattern immediately above matches the following:



```
def func1():  
    # ruleid: open-never-closed  
    fd = open('test.txt')  
    results = fd.read()  
    return results  
  
def func2():  
    # ok: open-never-closed  
    fd = open('test.txt')  
    results = fd.read()  
    fd.close()  
    return results  

```

The above rule looks for files that are opened but never closed, possibly leading to resource exhaustion. It looks for the `open(...)` pattern *and not* a following `close()` pattern.


The `$F` metavariable ensures that the same variable name is used in the `open` and `close` calls. The ellipsis operator allows for any arguments to be passed to `open` and any sequence of code statements in\-between the `open` and `close` calls. The rule ignores how `open` is called or what happens up to a `close` call—it only needs to make sure `close` is called.


Metavariable matching[​](#metavariable-matching "Direct link to Metavariable matching")
---------------------------------------------------------------------------------------


Metavariable matching operates differently for logical AND (`patterns`) and logical OR (`pattern-either`) parent operators. Behavior is consistent across all child operators: `pattern`, `pattern-not`, `pattern-regex`, `pattern-inside`, `pattern-not-inside`.


### Metavariables in logical ANDs[​](#metavariables-in-logical-ands "Direct link to Metavariables in logical ANDs")


Metavariable values must be identical across sub\-patterns when performing logical AND operations with the `patterns` operator.


Example:



```
rules:  
  - id: function-args-to-open  
    patterns:  
      - pattern-inside: |  
          def $F($X):  
              ...  
      - pattern: open($X)  
    message: "Function argument passed to open() builtin"  
    languages: [python]  
    severity: ERROR  

```

This rule matches the following code:



```
def foo(path):  
    open(path)  

```

The example rule doesn’t match this code:



```
def foo(path):  
    open(something_else)  

```

### Metavariables in logical ORs[​](#metavariables-in-logical-ors "Direct link to Metavariables in logical ORs")


Metavariable matching does not affect the matching of logical OR operations with the `pattern-either` operator.


Example:



```
rules:  
  - id: insecure-function-call  
    pattern-either:  
      - pattern: insecure_func1($X)  
      - pattern: insecure_func2($X)  
    message: "Insecure function use"  
    languages: [python]  
    severity: ERROR  

```

The above rule matches both examples below:



```
insecure_func1(something)  
insecure_func2(something)  

```


```
insecure_func1(something)  
insecure_func2(something_else)  

```

### Metavariables in complex logic[​](#metavariables-in-complex-logic "Direct link to Metavariables in complex logic")


Metavariable matching still affects subsequent logical ORs if the parent is a logical AND.


Example:



```
patterns:  
  - pattern-inside: |  
      def $F($X):  
        ...  
  - pattern-either:  
      - pattern: bar($X)  
      - pattern: baz($X)  

```

The above rule matches both examples below:



```
def foo(something):  
    bar(something)  

```


```
def foo(something):  
    baz(something)  

```

The example rule doesn’t match this code:



```
def foo(something):  
    bar(something_else)  

```

`options`[​](#options "Direct link to options")
-----------------------------------------------


Enable, disable, or modify the following matching features:




| Option | Default | Description |
| --- | --- | --- |
| `ac_matching` | `true` | [Matching modulo associativity and commutativity](https://semgrep.dev/docs/writing-rules/pattern-syntax#associative-and-commutative-operators), treat Boolean AND/OR as associative, and bitwise AND/OR/XOR as both associative and commutative. |
| `attr_expr` | `true` | Expression patterns (for example: `f($X)`) matches attributes (for example: `@f(a)`). |
| `commutative_boolop` | `false` | Treat Boolean AND/OR as commutative even if not semantically accurate. |
| `constant_propagation` | `true` | [Constant propagation](https://semgrep.dev/docs/writing-rules/pattern-syntax#constants), including [intra\-procedural flow\-sensitive constant propagation](https://semgrep.dev/docs/writing-rules/data-flow/constant-propagation). |
| `decorators_order_matters` | `false` | Match  non\-keyword attributes (for example: decorators in Python) in order,  instead of the order\-agnostic default. Keyword attributes (for example: `static`, `inline`, etc) are not affected. |
| `generic_comment_style` | none | In  generic mode, assume that comments follow the specified syntax. They  are then ignored for matching purposes. Allowed values for comment  styles are: * `c` for traditional C\-style comments (`/* ... */`). * `cpp` for modern C or C\+\+ comments (`// ...` or `/* ... */`). * `shell` for shell\-style comments (`# ...`).    By default, the generic mode does not recognize any comments. Available  since Semgrep version 0\.96\. For more information about generic mode,  see [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching) documentation. |
| `generic_ellipsis_max_span` | `10` | In generic mode, this is the maximum number of newlines that an ellipsis operator `...` can match or equivalently, the maximum number of lines covered by the match minus one. The default value is `10` (newlines) for performance reasons. Increase it with caution. Note that the same effect as `20` can be achieved without changing this setting and by writing `... ...` in the pattern instead of `...`. Setting it to `0` is useful with line\-oriented languages (for example [INI](https://en.wikipedia.org/wiki/INI_file)  or key\-value pairs in general) to force a match to not extend to the  next line of code. Available since Semgrep 0\.96\. For more information  about generic mode, see [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching) documentation. |
| `implicit_return` | `true` | Return statement patterns (for example `return $E`)  match expressions that may be evaluated last in a function as if there  was a return keyword in front of those expressions. Only applies to  certain expression\-based languages, such as Ruby and Julia. |
| `symmetric_eq` | `false` | Treat equal operations as symmetric (for example: `a == b` is equal to `b == a`). |
| `taint_assume_safe_functions` | `false` | Experimental option which will be subject to future changes. Used in taint analysis. Assume that function calls do **not**  propagate taint from their arguments to their output. Otherwise,  Semgrep always assumes that functions may propagate taint. Can replace **not\-conflicting** sanitizers added in v0\.69\.0 in the future. |
| `taint_assume_safe_indexes` | `false` | Used  in taint analysis. Assume that an array\-access expression is safe even  if the index expression is tainted. Otherwise Semgrep assumes that for  example: `a[i]` is tainted if `i` is tainted, even if `a`  is not. Enabling this option is recommended for high\-signal rules,  whereas disabling is preferred for audit rules. Currently, it is  disabled by default to attain backwards compatibility, but this can  change in the near future after some evaluation. |
| `vardef_assign` | `true` | Assignment patterns (for example `$X = $E`) match variable declarations (for example `var x = 1;`). |
| `xml_attrs_implicit_ellipsis` | `true` | Any XML/JSX/HTML element patterns have implicit ellipsis for attributes (for example: `<div />` matches `<div foo="1">`. |


The full list of available options can be consulted in the [Semgrep matching engine configuration](https://github.com/semgrep/semgrep/blob/develop/interfaces/Rule_options.atd)
 module. Note that options not included in the table above are 
considered experimental, and they may change or be removed without 
notice.


`fix`[​](#fix "Direct link to fix")
-----------------------------------


The `fix` top\-level key allows for simple autofixing of a pattern by suggesting an autofix for each match. Run `semgrep` with `--autofix` to apply the changes to the files.


Example:



```
rules:  
  - id: use-dict-get  
    patterns:  
      - pattern: $DICT[$KEY]  
    fix: $DICT.get($KEY)  
    message: "Use `.get()` method to avoid a KeyNotFound error"  
    languages: [python]  
    severity: ERROR  

```

For more information about `fix` and `--autofix` see [Autofix](https://semgrep.dev/docs/writing-rules/autofix) documentation.


`metadata`[​](#metadata "Direct link to metadata")
--------------------------------------------------


Provide additional information for a rule with the `metadata:` key, such as a related CWE, likelihood, OWASP.


Example:



```
rules:  
  - id: eqeq-is-bad  
    patterns:  
      - [...]  
    message: "useless comparison operation `$X == $X` or `$X != $X`"  
    metadata:  
      cve: CVE-2077-1234  
      discovered-by: Ikwa L'equale  

```

The metadata are also displayed in the output of Semgrep if you’re running it with `--json`.
Rules with `category: security` have additional metadata requirements. See [Including fields required by security category](https://semgrep.dev/docs/contributing/contributing-to-semgrep-rules-repository#including-fields-required-by-security-category) for more information.


`min-version` and `max-version`[​](#min-version-and-max-version "Direct link to min-version-and-max-version")
-------------------------------------------------------------------------------------------------------------


Each rule supports optional fields `min-version` and `max-version` specifying
minimum and maximum Semgrep versions. If the Semgrep
version being used doesn't satisfy these constraints,
the rule is skipped without causing a fatal error.


Example rule:



```
rules:  
  - id: bad-goflags  
    # earlier semgrep versions can't parse the pattern  
    min-version: 1.31.0  
    pattern: |  
      ENV ... GOFLAGS='-tags=dynamic -buildvcs=false' ...  
    languages: [dockerfile]  
    message: "We should not use these flags"  
    severity: WARNING  

```

Another use case is when a newer version of a rule works better than
before but relies on a new feature. In this case, we could use
`min-version` and `max-version` to ensure that either the older or the
newer rule is used but not both. The rules would look like this:



```
rules:  
  - id: something-wrong-v1  
    max-version: 1.72.999  
    ...  
  - id: something-wrong-v2  
    min-version: 1.73.0  
    # 10x faster than v1!  
    ...  

```

The `min-version`/`max-version` feature is available since Semgrep
1\.38\.0\. It is intended primarily for publishing rules that rely on
newly released features without causing errors in older Semgrep
installations.


`category`[​](#category "Direct link to category")
--------------------------------------------------


Provide a category for users of the rule. For example: `best-practice`, `correctness`, `maintainability`. For more information, see [Semgrep registry rule requirements](https://semgrep.dev/docs/contributing/contributing-to-semgrep-rules-repository#semgrep-registry-rule-requirements).


`paths`[​](#paths "Direct link to paths")
-----------------------------------------


### Excluding a rule in paths[​](#excluding-a-rule-in-paths "Direct link to Excluding a rule in paths")


To ignore a specific rule on specific files, set the `paths:` key with one or more filters. Paths are relative to the root directory of the scanned project.


Example:



```
rules:  
  - id: eqeq-is-bad  
    pattern: $X == $X  
    paths:  
      exclude:  
        - "**/*.jinja2"  
        - "*_test.go"  
        - "project/tests"  
        - project/static/*.js  

```

When invoked with `semgrep -f rule.yaml project/`, the above rule runs on files inside `project/`, but no results are returned for:


* any file with a `.jinja2` file extension
* any file whose name ends in `_test.go`, such as `project/backend/server_test.go`
* any file inside `project/tests` or its subdirectories
* any file matching the `project/static/*.js` glob pattern


noteThe glob syntax is from [Python's `wcmatch`](https://pypi.org/project/wcmatch/) and is used to match against the given file and all its parent directories.


### Limiting a rule to paths[​](#limiting-a-rule-to-paths "Direct link to Limiting a rule to paths")


Conversely, to run a rule *only* on specific files, set a `paths:` key with one or more of these filters:



```
rules:  
  - id: eqeq-is-bad  
    pattern: $X == $X  
    paths:  
      include:  
        - "*_test.go"  
        - "project/server"  
        - "project/schemata"  
        - "project/static/*.js"  
        - "tests/**/*.js"  

```

When invoked with `semgrep -f rule.yaml project/`, this rule runs on files inside `project/`, but results are returned only for:


* files whose name ends in `_test.go`, such as `project/backend/server_test.go`
* files inside `project/server`, `project/schemata`, or their subdirectories
* files matching the `project/static/*.js` glob pattern
* all files with the `.js` extension, arbitrary depth inside the tests folder


If you are writing tests for your rules, add any test file or directory to the included paths as well.


noteWhen mixing inclusion and exclusion filters, the exclusion ones take precedence.


Example:



```
paths:  
  include: "project/schemata"  
  exclude: "*_internal.py"  

```

The above rule returns results from `project/schemata/scan.py` but not from `project/schemata/scan_internal.py`.


Other examples[​](#other-examples "Direct link to Other examples")
------------------------------------------------------------------


This section contains more complex rules that perform advanced code searching.


### Complete useless comparison[​](#complete-useless-comparison "Direct link to Complete useless comparison")



```
rules:  
  - id: eqeq-is-bad  
    patterns:  
      - pattern-not-inside: |  
          def __eq__(...):  
              ...  
      - pattern-not-inside: assert(...)  
      - pattern-not-inside: assertTrue(...)  
      - pattern-not-inside: assertFalse(...)  
      - pattern-either:  
          - pattern: $X == $X  
          - pattern: $X != $X  
          - patterns:  
              - pattern-inside: |  
                  def __init__(...):  
                       ...  
              - pattern: self.$X == self.$X  
      - pattern-not: 1 == 1  
    message: "useless comparison operation `$X == $X` or `$X != $X`"  

```

The above rule makes use of many operators. It uses `pattern-either`, `patterns`, `pattern`, and `pattern-inside` to carefully consider different cases, and uses `pattern-not-inside` and `pattern-not` to whitelist certain useless comparisons.


Full specification[​](#full-specification "Direct link to Full specification")
------------------------------------------------------------------------------


The [full configuration\-file format](https://github.com/semgrep/semgrep-interfaces/blob/main/rule_schema_v1.yaml) is defined as
a [jsonschema](http://json-schema.org/specification.html) object.



---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/rule-syntax.md)Last updated on **Jul 24, 2024**[PreviousCustom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)[NextTesting rules](https://semgrep.dev/docs/writing-rules/testing-rules)* [Schema](#schema)
	+ [Required](#required)
	+ [Optional](#optional)
* [Operators](#operators)
	+ [`pattern`](#pattern)
	+ [`patterns`](#patterns)
	+ [`pattern-either`](#pattern-either)
	+ [`pattern-regex`](#pattern-regex)
	+ [`pattern-not-regex`](#pattern-not-regex)
	+ [`focus-metavariable`](#focus-metavariable)
	+ [`metavariable-regex`](#metavariable-regex)
	+ [`metavariable-pattern`](#metavariable-pattern)
	+ [`metavariable-comparison`](#metavariable-comparison)
	+ [`pattern-not`](#pattern-not)
	+ [`pattern-inside`](#pattern-inside)
	+ [`pattern-not-inside`](#pattern-not-inside)
* [Metavariable matching](#metavariable-matching)
	+ [Metavariables in logical ANDs](#metavariables-in-logical-ands)
	+ [Metavariables in logical ORs](#metavariables-in-logical-ors)
	+ [Metavariables in complex logic](#metavariables-in-complex-logic)
* [`options`](#options)
* [`fix`](#fix)
* [`metadata`](#metadata)
* [`min-version` and `max-version`](#min-version-and-max-version)
* [`category`](#category)
* [`paths`](#paths)
	+ [Excluding a rule in paths](#excluding-a-rule-in-paths)
	+ [Limiting a rule to paths](#limiting-a-rule-to-paths)
* [Other examples](#other-examples)
	+ [Complete useless comparison](#complete-useless-comparison)
* [Full specification](#full-specification)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Rule%20syntax%20_%20Semgrep_files/adsct_002.gif)![](Rule%20syntax%20_%20Semgrep_files/adsct.gif)









Troubleshooting rules \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Troubleshooting%20rules%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* Troubleshooting rules
On this page* [Troubleshooting](https://semgrep.dev/docs/tags/troubleshooting)
* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Troubleshooting rules
=====================


This page intends to help rule authors fix common mistakes when 
writing Semgrep rules. If you have a problem while running a rule you 
didn't write yourself, please [open a GitHub issue in the Semgrep Registry](https://github.com/semgrep/semgrep-rules/issues/new/choose) repository.


If your pattern can’t be parsed[​](#if-your-pattern-cant-be-parsed "Direct link to If your pattern can’t be parsed")
--------------------------------------------------------------------------------------------------------------------


This error means your pattern does not look like complete source code in the selected language.


"Complete source code" means that the Semgrep pattern must look like a valid, complete expression or statement on its own.


To illustrate with an example, Python isn't able to parse `if 4 < 5` as a line of code, because it's missing the code block on the right hand side.



```
>>> if 4 < 5  
  File "<stdin>", line 1  
    if 4 < 5  
            ^  
SyntaxError: invalid syntax  
>>>  

```

To get Python to parse this, you need to add a colon and a code block:



```
>>> if 4 < 5: print("it works!")  
...  
it works!  
>>>  

```

The same way Python's parser cannot parse partial statements or expressions, Semgrep cannot either.


The Semgrep pattern `if $X < 5` is invalid, and needs to be changed to a complete statement with a wildcard: `if $X < 5: ...`


While the most common reason for pattern parse errors is the above, other things to check would be:


* Make sure the correct language is selected
* If your pattern uses a metavariable, make sure it's all uppercase 
and does not start with a number. Valid metavariable names include `$X`, `$NAME`, and `$_VAR_2`. Invalid metavariable names include `$name`, `$1stvar` and `$VAR-WITH-DASHES`.


If your rule doesn't match where it should[​](#if-your-rule-doesnt-match-where-it-should "Direct link to If your rule doesn't match where it should")
-----------------------------------------------------------------------------------------------------------------------------------------------------


In general, it helps to test the patterns within your rule in 
isolation. If you scan for the patterns one by one and they each find 
what you expect, the issue is with the Boolean logic within your rule. 
Review the [rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
 to make sure the operators are meant to behave like you expect. If you 
managed to find a pattern that behaves incorrectly, continue debugging 
with the section below.


If your pattern doesn't match where it should[​](#if-your-pattern-doesnt-match-where-it-should "Direct link to If your pattern doesn't match where it should")
--------------------------------------------------------------------------------------------------------------------------------------------------------------


If you isolated the issue to one specific pattern, here are some common issues to look out for:


* When referencing something imported from a module, you need to fully qualify the import path. To match `import google.metrics; metrics.send(foo)` in Python, your pattern needs to be `google.metrics.send(...)` instead of `metrics.send(...)`.
* If your pattern uses a metavariable, make sure it's all uppercase 
and does not start with a number. Valid metavariable names include `$X`, `$NAME`, and `$_VAR_2`. Invalid metavariable names include `$name`, `$1stvar` and `$VAR-WITH-DASHES`.


If a regex pattern doesn't match where it should[​](#if-a-regex-pattern-doesnt-match-where-it-should "Direct link to If a regex pattern doesn't match where it should")
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


* When using `metavariable-regex`, the regex will match against all characters of the found metavariable. This means that if the metavariable matches a `"foo"` string in your code, the `metavariable-regex` pattern will run against a five character string with the quote characters at either end.
* Note that using the pipe (`|`) character will append a newline to your regex! If you are writing `pattern-regex: |` and then a newline with the regex, you almost certainly want the `|-` operator as in `pattern-regex: |-` to remove that trailing newline.


---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Troubleshooting](https://semgrep.dev/docs/tags/troubleshooting)
* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/troubleshooting/rules.md)Last updated on **Jun 18, 2024**[PreviousMetavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)[NextIntroduction](https://semgrep.dev/docs/writing-rules/experiments/introduction)* [If your pattern can’t be parsed](#if-your-pattern-cant-be-parsed)
* [If your rule doesn't match where it should](#if-your-rule-doesnt-match-where-it-should)
* [If your pattern doesn't match where it should](#if-your-pattern-doesnt-match-where-it-should)
* [If a regex pattern doesn't match where it should](#if-a-regex-pattern-doesnt-match-where-it-should)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Troubleshooting%20rules%20_%20Semgrep_files/adsct.gif)![](Troubleshooting%20rules%20_%20Semgrep_files/adsct_002.gif)









Data\-flow status \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Taint%20analysis%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
		- [Pattern syntax (Experimental)](https://semgrep.dev/docs/writing-rules/experiments/pattern-syntax)
		- [Aliengrep](https://semgrep.dev/docs/writing-rules/experiments/aliengrep)
		- [Displaying propagated value of metavariables](https://semgrep.dev/docs/writing-rules/experiments/display-propagated-metavariable)
		- [Extract mode](https://semgrep.dev/docs/writing-rules/experiments/extract-mode)
		- [Join mode](https://semgrep.dev/docs/writing-rules/experiments/join-mode/overview)
		- [Including multiple focus metavariables using set union semantics](https://semgrep.dev/docs/writing-rules/experiments/multiple-focus-metavariables)
		- [r2c\-internal\-project\-depends\-on](https://semgrep.dev/docs/writing-rules/experiments/r2c-internal-project-depends-on)
		- [Symbolic propagation](https://semgrep.dev/docs/writing-rules/experiments/symbolic-propagation)
		- [Matching captured metavariables with specific types](https://semgrep.dev/docs/writing-rules/experiments/metavariable-type)
		- [Deprecated experiments](https://semgrep.dev/docs/writing-rules/experiments/deprecated-experiments)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
		- [Constant propagation](https://semgrep.dev/docs/writing-rules/data-flow/constant-propagation)
		- [Taint analysis](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode)
		- [Data\-flow status](https://semgrep.dev/docs/writing-rules/data-flow/status)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
* Data\-flow status
* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Data\-flow status
=================


In principle, the data\-flow analysis engine (which provides taint 
tracking, constant propagation, and symbolic propagation) can run on any
 language [supported by Semgrep](https://semgrep.dev/docs/supported-languages). However, the level of support is lower than for the regular Semgrep matching engine.


When Semgrep performs an analysis of the code, it creates an **abstract syntax tree** (AST) which is then translated into an analysis\-friendly **intermediate language** (IL). Subsequently, Semgrep runs mostly language\-agnostic analysis on IL. However, this translation is not fully complete.


cautionThere
 can be features of some languages that Semgrep does not analyze 
correctly while using data\-flow analysis. Consequently, Semgrep does not
 fail even if it finds an unsupported construct. The analysis continues 
while the construct is ignored. This can result in Semgrep not matching 
some code that should be matched (false negatives) or matching a code 
that should not be matched (false positives).


Please, help us to improve and report any issues you encounter by creating an issue on Semgrep [GitHub](https://github.com/semgrep/semgrep/issues/new/choose) page.



---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/data-flow/status.md)Last updated on **Jun 12, 2024**[PreviousTaint analysis](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode)[NextSAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Taint%20analysis%20_%20Semgrep_files/adsct_002.gif)![](Taint%20analysis%20_%20Semgrep_files/adsct.gif)









SAST and rule\-writing glossary \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](SAST%20and%20rule-writing%20glossary%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
		- [Pattern syntax (Experimental)](https://semgrep.dev/docs/writing-rules/experiments/pattern-syntax)
		- [Aliengrep](https://semgrep.dev/docs/writing-rules/experiments/aliengrep)
		- [Displaying propagated value of metavariables](https://semgrep.dev/docs/writing-rules/experiments/display-propagated-metavariable)
		- [Extract mode](https://semgrep.dev/docs/writing-rules/experiments/extract-mode)
		- [Join mode](https://semgrep.dev/docs/writing-rules/experiments/join-mode/overview)
		- [Including multiple focus metavariables using set union semantics](https://semgrep.dev/docs/writing-rules/experiments/multiple-focus-metavariables)
		- [r2c\-internal\-project\-depends\-on](https://semgrep.dev/docs/writing-rules/experiments/r2c-internal-project-depends-on)
		- [Symbolic propagation](https://semgrep.dev/docs/writing-rules/experiments/symbolic-propagation)
		- [Matching captured metavariables with specific types](https://semgrep.dev/docs/writing-rules/experiments/metavariable-type)
		- [Deprecated experiments](https://semgrep.dev/docs/writing-rules/experiments/deprecated-experiments)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
		- [Constant propagation](https://semgrep.dev/docs/writing-rules/data-flow/constant-propagation)
		- [Taint analysis](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode)
		- [Data\-flow status](https://semgrep.dev/docs/writing-rules/data-flow/status)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* SAST and rule\-writing glossary
On this page* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Static analysis and rule\-writing glossary
==========================================


The definitions provided here are specific to Semgrep.


Constant propagation[​](#constant-propagation "Direct link to Constant propagation")
------------------------------------------------------------------------------------


Constant propagation is a type of analysis where values known to be 
constant are substituted in later uses, allowing the value to be used to
 detect matches. Semgrep can perform constant propagation across files, 
unless you are running Semgrep OSS, which can only propagate within a 
file.


Constant propagation is applied to all rules unless [it is disabled](https://semgrep.dev/docs/writing-rules/data-flow/constant-propagation#disabling-constant-propagation).


For example, given the following pattern:



```
...  
patterns:  
- pattern: console.log(2)  

```

And the following code snippet:



```
const x = 2;  
console.log(x);  

```

The pattern operator `pattern: print(2)` tells Semgrep to match line 2 because it propagates the value `2` from the assignment in line 1 to the `console.log()` function in line.


Constant propagation is one of the many analyses that differentiate Semgrep from grep.


Cross\-file analysis[​](#cross-file-analysis "Direct link to Cross-file analysis")
----------------------------------------------------------------------------------


Also known as **interfile analysis**. Cross\-file analysis takes into account how information flows between files. In particular, cross\-file analysis includes **cross\-file taint analysis**,
 which tracks unsanitized variables flowing from a source to a sink 
through arbitrarily many files. Other analyses performed across files 
include constant propagation and type inference.


Cross\-file analysis is usually used in contrast to intrafile (also 
known as per\-file analysis), where each file is analyzed as a standalone
 block of code.


Within Semgrep, cross\-file **and** cross\-function analysis is simply referred to as cross\-file analysis.


Semgrep OSS is limited to per\-file analysis.


Cross\-function analysis[​](#cross-function-analysis "Direct link to Cross-function analysis")
----------------------------------------------------------------------------------------------


Cross\-function analysis means that interactions between functions are
 taken into account. This improves taint analysis, which tracks 
unsanitized variables flowing from a source to a sink through 
arbitrarily many functions.


Within Semgrep documentation, cross\-function analysis implies 
intrafile or per\-file analysis. Each file is still analyzed as a 
standalone block, but within the file it takes into account how 
information flows between functions.


Also known as **interprocedural** analysis.


Error matrix[​](#error-matrix "Direct link to Error matrix")
------------------------------------------------------------


An error matrix is a 2x2 table that visualizes the findings of a 
Semgrep rule in relation to the vulnerable lines of code it does or 
doesn't detect. It has two axes:


* Positive and negative
* True or false


These yield the following combinations:


True positiveThe rule detected a piece of code it was intended to find.False positiveThe rule detected a piece of code it was not intended to find.True negativeThe rule correctly skipped over a piece of code it wasn't meant to find.False negativeThe rule failed to detect a piece of code it should have found.
Not to be confused with **risk matrices**.


Finding[​](#finding "Direct link to Finding")
---------------------------------------------


A finding is the core result of Semgrep's analysis. Findings are 
generated when a Semgrep rule matches a piece of code. Findings can be 
security issues, bugs, or code that doesn't follow coding conventions.


Fully qualified name[​](#fully-qualified-name "Direct link to Fully qualified name")
------------------------------------------------------------------------------------


A **fully qualified name** refers to a name which uniquely identifies a class, method, type, or module. Languages such as C\# and Ruby use `::` to distinguish between fully qualified names and regular names.


Not to be confused with **tokens**.


l\-value (left\-, or location\-value)[​](#l-value-left--or-location-value "Direct link to l-value (left-, or location-value)")
------------------------------------------------------------------------------------------------------------------------------


An expression that denotes an object in memory; a memory location, 
something that you can use in the left\-hand side (LHS) of an assignment.
 For example, `x` and `array[2]` are l\-values, but `2+2` is not.


Metavariable[​](#metavariable "Direct link to Metavariable")
------------------------------------------------------------


A metavariable is an abstraction that lets you match something even 
when you don't know exactly what it is you want to match. It is similar 
to capture groups in regular expressions. All metavariables begin with a
 `$` and can only contain uppercase characters, digits, and underscores.


Propagator[​](#propagator "Direct link to Propagator")
------------------------------------------------------


A propagator is any code that alters a piece of data as the data 
moves across the program. This includes functions, reassignments, and so
 on.


When you write rules that perform taint analysis, propagators are pieces of code that you specify through the `pattern-propagator`
 key as code that always passes tainted data. This is especially 
relevant when Semgrep performs intraprocedural taint analysis, as there 
is no way for Semgrep to infer which function calls propagate taint. 
Thus, explicitly listing propagators is the only way for Semgrep to know
 if tainted data could be passed within your function.


Rule (Semgrep rule)[​](#rule-semgrep-rule "Direct link to Rule (Semgrep rule)")
-------------------------------------------------------------------------------


A rule is a specification of the patterns that Semgrep must match to 
the code to generate a finding. Rules are written in YAML. Without a 
rule, the engine has no instructions on how to match code.


Rules can be run on either Semgrep or its OSS Engine. Only proprietary Semgrep can perform [interfile analysis](#cross-file-analysis).


There are two types of rules: **search** and **taint**.


Search rulesRules default to this type. Search rules
 detect matches based on the patterns described by a rule. There are 
several semantic analyses that search rules perform, such as:

* Interpreting syntactically different code as semantically equivalent
* Constant propagation
* Matching a fully qualified name to its reference in the code, even when not fully qualified
* Type inference, particularly when using typed metavariables
Taint rulesTaint
 rules make use of Semgrep's taint analysis in addition to default 
search functionalities. Taint rules are able to specify sources, sinks, 
and propagators of data as well as sanitizers of that data. For more 
information, see [Taint analysis documentation](https://semgrep.dev/writing-rules/data-flow/taint-mode/).
Sanitizers[​](#sanitizers "Direct link to Sanitizers")
------------------------------------------------------


A sanitizer is any piece of code, such as a function or [a cast](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/casting-and-type-conversions#explicit-conversions),
 that can clean untrusted or tainted data. Data from untrusted sources, 
such as user inputs, may be tainted with unsafe characters. Sanitizers 
ensure that unsafe characters are removed or stripped from the input.


An example of a sanitizer is the  [`DOMPurify.sanitize(dirty);`](https://github.com/cure53/DOMPurify) function from the DOMPurify package in JavaScript.


Per\-file analysis[​](#per-file-analysis "Direct link to Per-file analysis")
----------------------------------------------------------------------------


Also known as intrafile analysis. In per\-file analysis, information 
can only be traced or tracked within a single file. It cannot be traced 
if it flows to another file.


Per\-file analysis can include cross\-function analysis, aka tracing 
the flow of information between functions. When discussing the 
capabilities of pro analysis, per\-file analysis implies cross\-function 
analysis.


Per\-function analysis[​](#per-function-analysis "Direct link to Per-function analysis")
----------------------------------------------------------------------------------------


Also known as intraprocedural analysis. In per\-function analysis, 
information can only be traced or tracked within a single function.


Sink[​](#sink "Direct link to Sink")
------------------------------------


In taint analysis, a sink is any vulnerable function that is called with potentially tainted or unsafe data.


Source[​](#source "Direct link to Source")
------------------------------------------


In taint analysis, a source is any piece of code that assigns or sets tainted data, typically user input.


Taint analysis[​](#taint-analysis "Direct link to Taint analysis")
------------------------------------------------------------------


Taint analysis tracks and traces the flow of untrusted or unsafe 
data. Data coming from sources such as user inputs could be unsafe and 
used as an attack vector if these inputs are not sanitized. Taint 
analysis provides a means of tracing that data as it moves through the 
program from untrusted sources to vulnerable functions.



---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/glossary.md)Last updated on **May 22, 2024**[PreviousData\-flow status](https://semgrep.dev/docs/writing-rules/data-flow/status)* [Constant propagation](#constant-propagation)
* [Cross\-file analysis](#cross-file-analysis)
* [Cross\-function analysis](#cross-function-analysis)
* [Error matrix](#error-matrix)
* [Finding](#finding)
* [Fully qualified name](#fully-qualified-name)
* [l\-value (left\-, or location\-value)](#l-value-left--or-location-value)
* [Metavariable](#metavariable)
* [Propagator](#propagator)
* [Rule (Semgrep rule)](#rule-semgrep-rule)
* [Sanitizers](#sanitizers)
* [Per\-file analysis](#per-file-analysis)
* [Per\-function analysis](#per-function-analysis)
* [Sink](#sink)
* [Source](#source)
* [Taint analysis](#taint-analysis)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](SAST%20and%20rule-writing%20glossary%20_%20Semgrep_files/adsct_002.gif)![](SAST%20and%20rule-writing%20glossary%20_%20Semgrep_files/adsct.gif)






Advanced usage \| Testing Handbook

[LogoLogoTesting Handbook](https://appsec.guide/)
-------------------------------------------------

* [Static analysis](https://appsec.guide/docs/static-analysis/)
	+ [CodeQL](https://appsec.guide/docs/static-analysis/codeql/)
		- [Installation and first steps](https://appsec.guide/docs/static-analysis/codeql/installation/)
		- [Advanced usage](https://appsec.guide/docs/static-analysis/codeql/advanced/)
		- [Continuous integration](https://appsec.guide/docs/static-analysis/codeql/continuous-integration/)
		- [Additional resources](https://appsec.guide/docs/static-analysis/codeql/resources/)
	+ [Semgrep](https://appsec.guide/docs/static-analysis/semgrep/)
		- [Installation and first steps](https://appsec.guide/docs/static-analysis/semgrep/installation/)
		- [Advanced usage](https://appsec.guide/docs/static-analysis/semgrep/advanced/)
		- [Continuous integration](https://appsec.guide/docs/static-analysis/semgrep/continuous-integration/)
		- [In your organization](https://appsec.guide/docs/static-analysis/semgrep/in-your-organization/)
		- [Additional resources](https://appsec.guide/docs/static-analysis/semgrep/resources/)
* [Web application security](https://appsec.guide/docs/web/)
	+ [Burp Suite Professional](https://appsec.guide/docs/web/burp/)
		- [Step\-by\-step guide: rapidly mastering Burp to test your app](https://appsec.guide/docs/web/burp/guide/)
			* [Live task](https://appsec.guide/docs/web/burp/guide/livetask/)
			* [Working manually on specific HTTP requests](https://appsec.guide/docs/web/burp/guide/manual-work/)
				+ [Burp Repeater](https://appsec.guide/docs/web/burp/guide/manual-work/repeater/)
				+ [Burp Intruder](https://appsec.guide/docs/web/burp/guide/manual-work/intruder/)
				+ [Burp Collaborator](https://appsec.guide/docs/web/burp/guide/manual-work/collaborator/)
			* [Ensure your app handling works correctly](https://appsec.guide/docs/web/burp/guide/app-handling/)
		- [Additional Burp Best Practices and Tips](https://appsec.guide/docs/web/burp/tips/)
		- [Burp features vs. security issues](https://appsec.guide/docs/web/burp/bugs-vs-features/)
		- [Additional resources](https://appsec.guide/docs/web/burp/resources/)
* [Fuzzing](https://appsec.guide/docs/fuzzing/)
	+ [C/C\+\+](https://appsec.guide/docs/fuzzing/c-cpp/)
		- [libFuzzer](https://appsec.guide/docs/fuzzing/c-cpp/libfuzzer/)
		- [AFL\+\+](https://appsec.guide/docs/fuzzing/c-cpp/aflpp/)
		- Techniques
			* [Coverage analysis](https://appsec.guide/docs/fuzzing/c-cpp/techniques/coverage-analysis/)
			* [SUT patching: Overcoming obstacles](https://appsec.guide/docs/fuzzing/c-cpp/techniques/obstacles/)
	+ [Rust](https://appsec.guide/docs/fuzzing/rust/)
		- [cargo\-fuzz](https://appsec.guide/docs/fuzzing/rust/cargo-fuzz/)
		- Techniques
			* [Coverage analysis](https://appsec.guide/docs/fuzzing/rust/techniques/coverage-analysis/)
			* [SUT patching: Overcoming obstacles](https://appsec.guide/docs/fuzzing/rust/techniques/obstacles/)
			* [Writing harnesses](https://appsec.guide/docs/fuzzing/rust/techniques/writing-harnesses/)
	+ [Python](https://appsec.guide/docs/fuzzing/python/)
	+ [Ruby](https://appsec.guide/docs/fuzzing/ruby/)
	+ Techniques
		- [Writing harnesses](https://appsec.guide/docs/fuzzing/techniques/writing-harnesses/)
		- [Fuzzing dictionary](https://appsec.guide/docs/fuzzing/techniques/dictionary/)
		- [AddressSanitizer](https://appsec.guide/docs/fuzzing/techniques/asan/)
		- [Fuzzing environments](https://appsec.guide/docs/fuzzing/techniques/environments/)
		- [FAQ (Fuzzily Asked Questions)](https://appsec.guide/docs/fuzzing/techniques/faq/)
	+ [OSS\-Fuzz](https://appsec.guide/docs/fuzzing/oss-fuzz/)
	+ [Additional resources](https://appsec.guide/docs/fuzzing/resources/)
![Menu](Advanced%20usage%20_%20Testing%20Handbook_files/menu.svg)
**Advanced usage**
![Table of Contents](Advanced%20usage%20_%20Testing%20Handbook_files/toc.svg)* [Ignoring (parts of) code in your project with Semgrep](#ignoring-parts-of-code-in-your-project-with-semgrep)
	+ [Files/directories](#filesdirectories)
	+ [Excluding code sections](#excluding-code-sections)
* [Writing custom rules](#writing-custom-rules)
	+ [Example custom rule](#example-custom-rule)
	+ [Running custom rules](#running-custom-rules)
	+ [ABCs of writing custom rules](#abcs-of-writing-custom-rules)
	+ [Building blocks](#building-blocks)
	+ [Combining patterns](#combining-patterns)
	+ [Generic pattern matching](#generic-pattern-matching)
	+ [Metadata](#metadata)
	+ [Various tips](#various-tips)
	+ [Maintaining good quality of Semgrep rules](#maintaining-good-quality-of-semgrep-rules)
	+ [Help with writing custom rules](#help-with-writing-custom-rules)
* [Thoroughly testing Semgrep rules for optimal performance](#thoroughly-testing-semgrep-rules-for-optimal-performance)
	+ [Designing comprehensive test cases](#designing-comprehensive-test-cases)
* [Autofix feature](#autofix-feature)
	+ [Creating a Semgrep rule with the autofix feature](#creating-a-semgrep-rule-with-the-autofix-feature)
	+ [Regular expression\-based autofix](#regular-expression-based-autofix)
* [Optimizing Semgrep rules](#optimizing-semgrep-rules)
Advanced usage
[\#](#advanced-usage)
====================================

Ignoring (parts of) code in your project with Semgrep
[\#](#ignoring-parts-of-code-in-your-project-with-semgrep)
----------------------------------------------------------------------------------------------------------------

Semgrep identifies programming languages based on their file extensions rather than content analysis.
Use the `--scan-unknown-extensions` flag and the `--lang` flag to specify the language you want Semgrep
to use when scanning files with non\-standard extensions. For example:


```
semgrep --config /path/to/your/config --lang python --scan-unknown-extensions /path/to/your/file.xyz

```
In this example, Semgrep will scan the `/path/to/your/file.xyz` file as a Python file,
even though the `.xyz` extension is not a standard Python file extension.

See also the
[Allow user to specify file extensions for languages \#3090](https://github.com/returntocorp/semgrep/issues/3090)
GitHub issue to work around restrictions if you want to use Semgrep against your specific language, even if the file
extension is not standard.

### Files/directories
[\#](#filesdirectories)

* By default, Semgrep follows the default
[.semgrepignore](https://github.com/returntocorp/semgrep/blob/develop/cli/src/semgrep/templates/.semgrepignore) file.
* If present, Semgrep will look at the repository’s `.gitignore` file.
* In case of a conflict between the two files, the `.semgrepignore` file takes precedence. This means that if the
`.gitignore` file includes a file and the `.semgrepignore` file excludes it, Semgrep will not analyze the file.

Before starting a scan, it is recommended that you review the files and directories in your project directory.
Note that certain paths may be excluded by default. If you want to change the default exclusion behavior,
such as including third\-party libraries or unit tests in the scan, you can create a custom `.semgrepignore` file.

### Excluding code sections
[\#](#excluding-code-sections)

To prevent Semgrep from flagging incorrect code patterns, insert a comment in your code immediately before or on the line
preceding the pattern match (e.g., `// nosemgrep: rule-id`). It is crucial to have a space between `//` and `nosemgrep`.

As a best practice, remember to:

* Exclude only particular findings in your comments rather than disabling all rules with a generic `// nosemgrep` comment.
* Explain why you disabled a rule or justify your risk acceptance decision.
* If you encounter a false positive and want to ignore a Semgrep rule, provide feedback to either the Semgrep development
team or your internal development team responsible for the specific rule. This will help improve the accuracy
of the rule and reduce the chances of future false positives.

For more information on how to use `nosemgrep` to ignore code blocks for a particular rule, refer to the
[Semgrep documentation on ignoring code](https://semgrep.dev/docs/ignoring-files-folders-code/#ignoring-code-through-nosemgrep).

Writing custom rules
[\#](#writing-custom-rules)
------------------------------------------------

While Semgrep offers a library of pre\-built rules, creating custom rules can significantly enhance your security testing
by tailoring it to your specific codebase and requirements. However, creating effective Semgrep rules can be challenging
without proper guidance and understanding. This section will give you the essential knowledge and skills to create
high\-quality Semgrep rules. You will learn about the rule language’s syntax and how to develop effective patterns,
handle edge cases, and create powerful custom Semgrep rules. This will aid in detecting potential security vulnerabilities
early on, ultimately improving your testing process.

### Example custom rule
[\#](#example-custom-rule)

As a starting point for creating a custom rule, use the following schema to create the `custom_rule.yaml` file.


```
1rules:
2  - id: rule-id
3    languages: [go]
4    message: Some message
5    severity: ERROR # INFO / WARNING / ERROR
6    pattern: test(...)

```
### Running custom rules
[\#](#running-custom-rules)

* To run the above\-mentioned rule as a single file, use the following command:


```
semgrep --config custom_rule.yaml

```
* To run a set of rules in a directory:


```
semgrep --config path/

```
### ABCs of writing custom rules
[\#](#abcs-of-writing-custom-rules)

To start writing custom Semgrep rules, it is crucial to understand a few key concepts and tools:

1. **Familiarize yourself with Semgrep syntax**: Begin by exploring the official
[Learn Semgrep Syntax](https://semgrep.dev/learn)
page, which provides a comprehensive guide on the fundamentals of Semgrep rule writing.
2. **Refer to language\-specific pattern examples**: Consult the
[Semgrep Pattern Examples by Language](https://semgrep.dev/embed/cheatsheet)
for examples tailored to specific programming languages.
3. **Use the Semgrep Playground**: The
[Semgrep Playground](https://semgrep.dev/playground/new) is a convenient online tool
for writing and testing rules. However, it is essential to consider the following points when using the Playground:
> **Be cautious of privacy concerns**: The Semgrep Playground allows users to experiment with code
> without downloading or installing software on their local machine. While this platform is helpful for testing
> and debugging rules, it may expose sensitive information such as passwords, API keys, or other secrets contained
> in the code you submit for scanning.
> Always use a local development environment with proper security and privacy controls for sensitive code.


	* **Employ the `simple mode`**: The Semgrep Playground’s simple mode makes it easy to combine rule patterns.
	* **Use the `Share` button**: Share your rule and test code with others using the Share button.
	* **Add tests to your test code**: Incorporate
	[tests](https://semgrep.dev/docs/writing-rules/testing-rules/)
	(e.g., `# ruleid: <id>`) into your test code to evaluate your rule’s effectiveness while working in the Semgrep
	Playground (see
	[example](https://semgrep.dev/s/ezxE)).
	* **Note the limitations with comments**: Be aware that the Semgrep Playground does not retain comments when sharing
	a link or “forking” a rule (Ctrl\+S). Refer to this
	[GitHub issue](https://github.com/returntocorp/semgrep/issues/7120)
	for more information.

### Building blocks
[\#](#building-blocks)

#### Ellipses (`...`)
[\#](#ellipses-)


> **Purpose**: The ellipsis (`...`) is used to match zero or more arguments, statements, parameters,
> and so on, allowing for greater flexibility in pattern matching.

Here is an example rule for Python:


```
1rules:
2  - id: rule-id
3    languages: [Python]
4    message: Some message
5    severity: INFO
6    pattern: requests.get(..., verify=False, ...)

```
Here, the ellipsis before and after the `verify=False` argument allows the pattern to match
any number of arguments before and after the `verify` parameter. This ensures that the pattern
can match function calls with various argument combinations, as long as the `verify=False` argument is present.

This pattern matches the following code snippets:


```
1requests.get(verify=False, url=URL)
2requests.post(verify=False, url=URL)
3requests.get(URL, verify=False, timeout=3)
4requests.head()
5requests.get(URL)
6requests.get(URL, verify=False)

```
In the second example, the ellipsis is used to create a pattern that matches an `if` statement
followed by an unnecessary `else` block after a `return` statement within the `if` block.

Below is the `unnecessary-if-else-pattern` rule for Python:


```
 1rules:
 2  - id: unnecessary-if-else-pattern
 3    languages: [Python]
 4    message: Unnecessary else after return $X
 5    severity: INFO
 6    pattern: |
 7      if ...:
 8        return ...
 9      else:
10        ...      

```
Now, let’s break down the pattern components:

1. `if ...:`: This part of the pattern matches any `if` statement, regardless of the condition being tested.
The ellipsis within the `if` statement is a wildcard that matches any expression or code structure used as the condition.
This flexibility ensures that the pattern can detect a wide range of `if` statements with various conditions.
2. `return ...`: Within the matched `if` block, the `return` statement is followed by an ellipsis. This wildcard matches
any expression or value being returned. This allows the pattern to detect `return` statements with different values or
expressions, such as `return True`, `return False`, `return x`, or `return calculate_result()`.
3. `...` within the `else` block: The ellipsis in the `else` block is a wildcard that matches any number of statements.

This pattern matches the following code snippet:


```
1if a > b:
2  return True
3else:
4  print("a is not greater than b")

```
By including the ellipsis (`...`) in your Semgrep rules, you can create more flexible and comprehensive patterns that account
for variations in code structure.

#### Metavariables
[\#](#metavariables)


> **Purpose**: Metavariables are used to match and track values across a specific code scope.
> They are denoted by a dollar sign followed by a capitalized letters (e.g., `$X`, `$Y`, `$COND`).

Here is an example pattern in Golang:


```
pattern: $X.($TYPE)

```
The metavariable `$X` matches:


```
1msg, ok := m.(*MsgDonate) // $X = m
2p := val.(types.Pool) // $X = val
3x := val
4msg, ok = m

```
Metavariables can also be interpolated into the output message of a Semgrep rule.
For instance, consider the following rule:


```
1rules:
2  - id: metavariable-example-rule
3    patterns:
4      - pattern: func $X(...) { ... }
5    message: Found $X function
6    languages: [golang]
7    severity: WARNING

```
For the following code:


```
1func test123(input string) {
2    fmt.Println("test")
3}

```
This returns the `Found test123 function` message in the Semgrep output, as follows:


```
$ semgrep -f rule.yml
# (...)
     metavariable-example-rule
        Found test123 function

          1┆ func test123(input string) {
          2┆     fmt.Println("test")
          3┆ }

```
Metavariables help create more dynamic and versatile Semgrep rules by capturing values that can be used for further
pattern matching or validation.

##### Leveraging metavariables
[\#](#leveraging-metavariables)

Metavariables can be used in a variety of ways to enhance Semgrep rules, making
them more dynamic and adaptable when analyzing code. Some common use cases include:

1. **Matching variable names**: Metavariables can be used to match variable names in the code,
allowing the rule to be flexible and applicable to various situations. For example:


```
pattern: $X := $Y

```
This pattern would match assignments like `a := b` or `result := calculation()`.
2. **Capturing function calls**: Metavariables can be employed to capture function calls and their arguments.
This can be useful for detecting potentially unsafe or deprecated functions. For example:


```
pattern: $FUNC($ARG)

```
This pattern would match function calls like `dangerousFunc(input)` or `deprecatedFunc(arg1, arg2)`.
3. **Matching control structures**: Metavariables can help identify specific control structures,
such as loops or conditionals, with a particular focus on the expressions used within these structures. For example:


```
pattern: for $INDEX := $INIT; $COND; $UPDATE { ... }

```
This pattern would match for\-loops like `for i := 0; i < 10; i++ { ... }`.
4. **Comparing code patterns**: Metavariables can be used to compare different parts of the code to ensure consistency
or prevent potential bugs. For example, you can detect cases where the same assignment is
made in both branches of an `if-else` statement:


```
pattern: if $COND { $X = $Y } else { $X = $Y }

```
This pattern would match code like:


```
1if someCondition {
2    x = y
3} else {
4    x = y
5}

```
5. **Identifying patterns across multiple lines**: Metavariables can be employed to match and track values
across multiple lines of code, making it possible to detect patterns that span several statements. For example:


```
pattern: |
  $VAR1 := $EXPR1
  $VAR2 := $VAR1  

```
This pattern would match code like the following:


```
1a := b + c
2d := a

```

In conclusion, metavariables offer a powerful way to create dynamic and adaptable Semgrep rules. They help capture
and track values across code scopes, enabling the identification of complex patterns and providing informative output
messages for developers and security professionals.

#### Nested metavariables
[\#](#nested-metavariables)


> **Purpose**: Nested metavariables allow you to match a pattern with a metavariable that also contains
> another metavariable meeting certain conditions.

Here is an example rule:


```
 1rules:
 2  - id: metavariable-pattern-nest
 3    languages: [python]
 4    message: substraction in foo(bar(...))
 5    patterns:
 6      - pattern: foo($X, ...)
 7      # First metavariable-pattern
 8      - metavariable-pattern:
 9          metavariable: $X
10          patterns:
11            - pattern: bar($Y)
12            # Nested metavariable pattern
13            - metavariable-pattern:
14                metavariable: $Y
15                patterns:
16                  - pattern: ... - ...
17    severity: WARNING

```
This rule matches the following Python code:


```
1foo(bar(1-2))
2foo(bar(bar(1-2)))

```
Nested metavariables allow for more complex and precise pattern matching in Semgrep rules by allowing you to define
relationships between multiple metavariables.

#### Using `metavariable-pattern` for polyglot file scanning
[\#](#using-metavariable-pattern-for-polyglot-file-scanning)


> **Purpose**: To match patterns across different languages within a single file
> (e.g., JavaScript embedded in HTML).

Example: Find all instances of JavaScript’s
[eval](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval)
function used in an HTML file (
[example](https://semgrep.dev/s/W9by)).


```
 1rules:
 2  - id: metavariable-pattern-nest
 3    languages: [html]
 4    message: eval in JS
 5    patterns:
 6      - pattern: <script ...>$Y</script>
 7      - metavariable-pattern:
 8          metavariable: $Y
 9          language: javascript
10          patterns:
11            - pattern: eval(...)
12    severity: WARNING

```
This rule matches the following HTML code:


```
1<script>
2    console.log('test123');
3    eval(1+1);
4</script>

```
Using `metavariable-pattern` allows for cross\-language pattern matching in polyglot files, enabling you to identify
specific code patterns within mixed\-language files.

#### Using `metavariable-pattern` \+ `pattern-either`
[\#](#using-metavariable-pattern--pattern-either)


> **Purpose**: To specify multiple alternative patterns
> that can match a metavariable.

Example: Flag instances where a variable declaration uses one of several specific types
(
[example](https://semgrep.dev/s/J0zk)
/
[trailofbits.go.string\-to\-int\-signedness\-cast.string\-to\-int\-signedness\-cast](https://semgrep.dev/playground/r/trailofbits.go.string-to-int-signedness-cast.string-to-int-signedness-cast?editorMode=advanced)
rule).


```
 1rules:
 2  - id: metavariable-pattern-multiple-or
 3    languages: [go]
 4    message: xyz
 5    patterns:
 6      - pattern: var $A $TYPE = ...
 7      - metavariable-pattern:
 8          metavariable: $TYPE
 9          pattern-either:
10            - pattern: uint8
11            - pattern: uint16
12            - pattern: uint32
13            - pattern: int8
14            - pattern: int16
15            - pattern: int32
16    severity: WARNING

```
This rule matches the following Go code:


```
1var a uint8 = 255
2var b uint16 = 65535
3var c uint32 = 4294967295
4var d int8 = -128
5var e int16 = -32768
6var f int32 = -2147483648
7var g string = "xyz"

```
Combining `metavariable-pattern` with `pattern-either` allows you to create Semgrep rules that match a `metavariable` if
it meets any of the specified conditions.

#### Metavariable\-pattern \+ patterns
[\#](#metavariable-pattern--patterns)


> **Purpose**: Use `metavariable-pattern` and `patterns` to flag instances where a metavariable `$X`
> meets *all* conditions (`patterns`) (
> [example](https://semgrep.dev/s/BJqv) /
> [lxml\-in\-pandas rule](https://semgrep.dev/playground/r/trailofbits.python.lxml-in-pandas.lxml-in-pandas?editorMode=advanced))

Here is an example rule:


```
 1rules:
 2  - id: metavariable-pattern-and-patterns
 3    languages:
 4      - go
 5    message: xyz1
 6    patterns:
 7      - pattern: var $A $TYPE = $Z
 8      - metavariable-pattern:
 9          metavariable: $Z
10          patterns:
11            - pattern-not: |
12                  -128                  
13            - pattern-not: |
14                  -32768                  
15    severity: WARNING

```
This rule matches the following Go code:


```
1var b uint16 = 65535
2var d int8 = -128
3var c uint32 = 4294967295
4var e int16 = -32768

```
#### Constant propagation
[\#](#constant-propagation)

Constant propagation in Semgrep refers to the process of matching instances where a `metavariable` holds a specific value
or relation.

##### Matching instances where a metavariable holds a specific value
[\#](#matching-instances-where-a-metavariable-holds-a-specific-value)


> **Purpose**: To match instances where a metavariable holds a specific value or relation, use
> the `metavariable-comparison` key.

Example: Match cases where the variable `$X` is greater than `1337` (
[example](https://semgrep.dev/s/LqeL)).


```
 1rules:
 2  - id: metavariable-comparison
 3    languages: [python]
 4    message: $X is higher than 1337
 5    patterns:
 6      - pattern: function($X)
 7      - metavariable-comparison: # Match when $X > 1337
 8          metavariable: $X
 9          comparison: $X > 1337
10    severity: WARNING

```
This rule matches the following Python code:


```
1n = 1339
2function(n) # Match (n > 1337)
3function(1338) # Match (constant > 1337)
4function(123)

```
##### Comparing specific metavariables
[\#](#comparing-specific-metavariables)


> **Purpose**: Compare specific metavariables.

Example: Match functions where the first argument is lower than the second one (
[example](https://semgrep.dev/s/dYnd)).


```
 1rules:
 2  - id: metavariable-comparison-rule
 3    patterns:
 4      - pattern: f($A, $B)
 5      - metavariable-comparison:
 6          comparison: int($A) < int($B)
 7          metavariable: $A
 8    message: $A < $B
 9    languages: [python]
10    severity: WARNING

```
This rule matches the following Python code:


```
1f(1,2)
2f(2,3)
3f(4,3)
4f(12312,1)

```
#### Deep expression operator
[\#](#deep-expression-operator)


> **Purpose**: To match deeply nested expressions in the code.

Deep expression operator is useful when you want to identify specific patterns that are buried within complex structures
like conditional statements, loops, or function calls. Using the deep expression operator, you can create rules that
target specific code patterns regardless of how deep they are in the code structure.The deep expression operator is represented by `<... ...>`. It acts as a wildcard that matches any code structure between
the opening and closing ellipses. By using the deep expression operator, you can create Semgrep rules that match patterns
in any level of nesting.

**Example**: Matching a function call nested within an `if` statement (
[example](https://semgrep.dev/s/2Qv8)).

Suppose you want to match any instance of a specific function call (e.g., `user.is_admin()`) within an `if` statement,
regardless of how deeply nested it is.


```
1rules:
2- id: deep-expression-example
3  pattern: |
4      if <... user.is_admin() ...>:
5        print(...)      
6  message: if statement with is_admin() check
7  languages: [python]
8  severity: WARNING

```
This rule matches the following Python code:


```
1if user.authenticated() and user.is_admin() and user.has_group(gid):
2    print("hello")

```
#### Understanding `pattern-inside` and `pattern-not-inside`
[\#](#understanding-pattern-inside-and-pattern-not-inside)

##### Using `pattern-inside`
[\#](#using-pattern-inside)

By using `pattern-inside`, you can create rules that match patterns only when they appear
**within** a certain code construct, like a function, or class definition, a loop, or a conditional block.

Here’s an example of how you might use `pattern-inside` to detect cases where a sensitive function is called within a loop:


```
 1rules:
 2- id: sensitive_function_in_loop
 3  languages:
 4    - python
 5  message: "Sensitive function called inside a loop"
 6  severity: WARNING
 7  patterns:
 8    - pattern-inside: |
 9        for ... in ...:
10            ...        
11    - pattern: |
12        sensitive_function(...)        

```
In this example, the `pattern-inside` operator is used to match any `for` loop in Python, and the second
pattern matches calls to `sensitive_function()`. The rule will trigger only if both patterns are matched,
meaning that the `sensitive_function` is called **inside** a loop.

Here’s an example of Python code that would trigger the `sensitive_function_in_loop` rule:


```
 1def sensitive_function(data):
 2    # Process sensitive data
 3    pass
 4
 5def main():
 6    data_list = ['data1', 'data2', 'data3']
 7
 8    for data in data_list:
 9        # Call to sensitive_function is inside a loop
10        sensitive_function(data)
11
12def second(data):
13    sensitive_function(data)

```
##### Using `pattern-not-inside`
[\#](#using-pattern-not-inside)

`pattern-not-inside` is the opposite of `pattern-inside` and is used to match a pattern only when it
**does not appear** within a specified context. This operator helps you to exclude certain parts of the
code from your analysis, further refining your rules and reducing false positives.

For instance, you can use `pattern-not-inside` to detect calls to the `print_debug()`
function when they occur outside a `if debug:` block:


```
 1rules:
 2- id: print_debug_outside_debug_block
 3  languages:
 4    - python
 5  message: "print_debug() should be called inside a 'if debug:' block"
 6  severity: WARNING
 7  patterns:
 8    - pattern-not-inside: |
 9        if debug:
10            ...        
11    - pattern: |
12        print_debug(...)        

```
Here is a Python code example demonstrating the use of this rule:


```
 1debug = True
 2
 3def print_debug(msg):
 4    print("DEBUG:", msg)
 5
 6def correct_usage():
 7    if debug:
 8        print_debug("This is a debug message inside a 'if debug:' block")
 9
10def incorrect_usage():
11    print_debug("This is a debug message outside a 'if debug:' block")
12
13def main():
14    correct_usage()
15    incorrect_usage()

```
##### Combining `pattern-inside` and `pattern-not-inside`
[\#](#combining-pattern-inside-and-pattern-not-inside)

In some cases, you might want to create rules that use both `pattern-inside`
and `pattern-not-inside` operators to capture instances where a specific pattern
is found within a particular context but not within another.

**Example**: Detecting `print()` calls in functions but not in `main()`.

Suppose you want to enforce a rule where `print()` calls are allowed only within
the `main()` function and not in any other functions. You can create a rule that
combines `pattern-inside` and `pattern-not-inside` operators to achieve this.


```
 1rules:
 2- id: print_calls_outside_main
 3  languages:
 4    - python
 5  message: "print() calls should only be inside the main() function"
 6  severity: WARNING
 7  patterns:
 8    - pattern-inside: |
 9        def $X(...):
10            ...        
11    - pattern-not-inside: |
12        def main(...):
13            ...        
14    - pattern: |
15        print(...)        

```
In this example, the `pattern-inside` operator matches any function definition, while
the `pattern-not-inside` operator ensures that the `main()` function is excluded.
The final pattern matches calls to the `print()` function. The rule will trigger only
when a `print()` call is found inside a function other than `main()`.

Here’s an example of Python code that triggers the `print_calls_outside_main` rule:


```
 1def sample_function():
 2    # print() call inside a function other than main()
 3    print("This is a sample function")
 4
 5def main():
 6    print("This is the main function")
 7    sample_function()
 8
 9def other_function():
10    some_function()
11    print("XYZ")

```
#### Taint mode
[\#](#taint-mode)

Taint mode is a powerful feature in Semgrep that can track the flow of data from one location to another.
By using taint mode, you can:

1. **Track data flow across multiple variables:** Taint mode enables you to trace how data moves across different variables,
functions, components, and allows you to easily identify insecure flow paths (e.g., situations where a specific sanitizer
is not used).
2. **Find injection vulnerabilities:** Taint mode is particularly useful for identifying injection vulnerabilities such as
SQL injection, command injection, and XSS attacks.
3. **Write simple and resilient Semgrep rules:** Taint mode simplifies the process of writing Semgrep rules that are resilient
to certain code patterns nested in `if` statements, loops, and other structures.

To use taint mode, you need to set the `mode: taint` and specify `pattern-sources`/`pattern-sinks` fields in your custom
Semgrep rule.

See this
[example](https://semgrep.dev/s/el3X):


```
 1rules:
 2  - id: taint-tracking-example1
 3    mode: taint
 4    pattern-sources:
 5      - pattern: getData()
 6    pattern-sinks:
 7      - pattern: printToUser(...)
 8    message: data flows from getData to printToUser
 9    languages: [python]
10    severity: WARNING

```
Optionally, you can use additional fields in your Semgrep rule to further refine your taint analysis:

* `pattern-propagators`: This field allows you to specify functions or methods that propagate tainted data
(
[example](https://semgrep.dev/s/7Nrv)). You can also refer to
[sanitizers by side\-effect](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode/#sanitizers-by-side-effect) for
more information.
* `pattern-sanitizers`: This field allows you to specify functions or methods that sanitize tainted data.
For more information, see the
[taint mode documentation](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode/#propagators).

### Combining patterns
[\#](#combining-patterns)

When writing Semgrep rules, you may encounter situations where a single pattern (e.g., `pattern: evil_function(...)`)
isn’t sufficient to capture the behavior you want to detect. In these cases, you can use one of the following to combine
patterns:

* `patterns`: This method combines multiple patterns with a logical AND (\&\&). In other words,
all patterns must match for the rule to trigger. This is useful when you want to detect code snippets that satisfy
multiple conditions simultaneously.
* `pattern-either`: This method combines multiple patterns with a logical OR (\|\|). In other words, if any of the
patterns match, the rule triggers. This is useful when you want to detect code snippets satisfying at least one
specified condition.

Suppose you want to detect calls to two insecure functions, `insecure_function_1()` and `insecure_function_2()`.
You can use the `pattern-either` operator to achieve this.


```
 1rules:
 2- id: insecure_function_calls
 3  languages:
 4    - python
 5  message: "Call to an insecure function detected"
 6  severity: WARNING
 7  patterns:
 8    - pattern-either:
 9        - pattern: |
10            insecure_function_1(...)            
11        - pattern: |
12            insecure_function_2(...)            

```
In this example, the `pattern-either` operator is used to match calls to either `insecure_function_1()`
or `insecure_function_2()`. The rule will trigger if any of these patterns are matched.

Here’s an example of Python code that triggers the `insecure_function_calls` rule:


```
 1def insecure_function_1():
 2    print("Insecure function 1 called")
 3
 4def insecure_function_2():
 5    print("Insecure function 2 called")
 6
 7def main():
 8    # Call to insecure_function_1() triggers the rule
 9    insecure_function_1()
10
11    # Call to insecure_function_2() also triggers the rule
12    insecure_function_2()

```
* `pattern-regex`: This matches code with a
[PCRE](https://www.pcre.org/original/doc/html/pcrepattern.html)\-compatible
pattern in multiline mode. In other words, it matches code using a regular expression pattern.

#### Rule syntax diagram
[\#](#rule-syntax-diagram)

The following diagram will help you understand the relationship between the relevant fields in the rule. While writing
a rule, you can use the advanced mode in the
[Semgrep Playground](https://semgrep.dev/playground/new) to test
and refine it. The playground highlights any errors in your rules, providing immediate feedback.

Only one is allowedOnly one is requiredRule FieldsRequiredidmessageseveritylanguagesPattern Fieldspatternpattern\-regexpattern\-eitherpatternspattern\-insidemetavariable\-patternmetavariablelanguagemetavariable\-regexmetavariableregexmetavariable\-comparisonmetavariablecomparisonbasestrippattern\-notpattern\-not\-insidepattern\-not\-regexOptionaloptionsfixmetadatapaths

**Example \#1**:
Looking at the chart, you can see that the `pattern-either` and `pattern-not` fields are not directly connected.
However, you can combine them using the `patterns` field, which performs a logical AND operation on all the patterns included.

**Example \#2**:
For instance, if you want to use `pattern-either` to combine multiple patterns with a logical OR and exclude a specific
pattern using `pattern-not`, you can do so by including both of them under the same `patterns` field.
The resulting combination of patterns will match only code that satisfies all of the patterns included in
the `pattern-either` field, except for the pattern specified in `pattern-not`.
See the example
[`exclude-when-using-secure-option`](https://semgrep.dev/s/vgob) rule.

### Generic pattern matching
[\#](#generic-pattern-matching)

It is possible to match generic patterns in unsupported languages/contexts.
Use the `generic` language for configuration files, XML, etc., and combine it with the specific extension
through the `paths` \- `include` fields to reduce false positives.

For example, see the
[`nsc-allows-plaintext-traffic`
rule](https://semgrep.dev/playground/r/java.android.best-practice.network-security-config.nsc-allows-plaintext-traffic?editorMode=advanced),
which scans the Android manifest XML file for potential misconfiguration:


```
 1rules:
 2  - id: nsc-allows-plaintext-traffic
 3    languages: [generic]
 4    patterns:
 5      - pattern: |
 6          <base-config ... cleartextTrafficPermitted="true" ... >          
 7      - pattern-not-inside: |
 8          <!-- ... -->          
 9      - pattern-not-inside: >
10          <network-security-config ... InsecureBaseConfiguration ... > ... ...
11          ... ... ... ... ... ... ... ... </network-security-config>          
12    severity: INFO
13    paths:
14      include:
15        - "*.xml"

```
### Metadata
[\#](#metadata)

Metadata fields are a feature in Semgrep that allow you to attach additional information to your rules.
By including metadata fields in your rules, you can give developers more context and guidance on addressing potential issues.
This information can include details such as the rule’s severity level, recommended fixes, or the author’s contact information.
By including metadata, you can make your rules more informative and actionable for developers who encounter them.
This can help them prioritize and fix issues more efficiently, ultimately improving the overall security of your codebase.

In addition to providing context and guidance to developers, there are several other reasons why an organization
might want to use Semgrep metadata:

1. **Standardization.** Using metadata fields consistently across all of your organization’s Semgrep rules ensures that
developers see the same types of information and recommendations no matter which rules they encounter.
This can help standardize the security review process and simplify prioritizing and addressing issues.
	* Example:
	[By including fields required by the security category in the Semgrep Registry](https://semgrep.dev/docs/contributing/contributing-to-semgrep-rules-repository/#including-fields-required-by-security-category),
	developers will prioritize findings with high `confidence` and high `impact` metadata.
2. **Collaboration.** Including author information in your Semgrep rules can make it easier for other organization members
to collaborate on security issues.
	* Example: Suppose someone has a question or needs more information about a particular rule. In that case, they can
	contact the `author` directly for clarification.
3. **Compliance.** Suppose your organization needs to comply with specific security regulations or standards.
In this case, you could include a `compliance` metadata field in your Semgrep rules, indicating which regulation or
standard the rule relates to. This helps ensure that your codebase complies with all relevant requirements.

You can create any metadata field, as demonstrated in the
[hooray\-taint\-mode](https://semgrep.dev/playground/s/4K3g) rule.

We recommend including the following metadata fields required by the security category in the Semgrep Registry:

1. `cwe`: A
[Common Weakness Enumeration](https://cwe.mitre.org/index.html) identifier that classifies the security issue.
2. `confidence`: An assessment of the rule’s accuracy, represented as high, medium, or low.
3. `likelihood`: An estimation of the probability that the detected issue will be exploited, represented as high,
medium, or low.
4. `impact`: A measure of the potential damage caused by exploiting the detected issue, represented as high, medium, or low.
5. `subcategory`: A more specific classification of the rule, falling under one of the following categories:
[vuln, audit, or guardrail](https://semgrep.dev/docs/contributing/contributing-to-semgrep-rules-repository/#subcategory).

By including these metadata fields, you provide valuable context and help users better understand the security
implications of the issues detected by your rule.

### Various tips
[\#](#various-tips)

#### Matching an array with a non\-string element
[\#](#matching-an-array-with-a-non-string-element)

This Semgrep rule aims to detect JavaScript or TypeScript arrays that contain at least one non\-string element.
See this
[array\-with\-a\-non\-string\-element example](https://semgrep.dev/s/BJnb).


```
 1rules:
 2  - id: array-with-a-non-string-element
 3    languages: [js]
 4    message: array with element that is not a string
 5    severity: WARNING
 6    patterns:
 7      - metavariable-pattern:
 8          metavariable: $A
 9          patterns:
10            - pattern-not: "..."
11      - pattern: [..., $A, ...]

```
#### “Removing” negative pattern from pattern\-either
[\#](#removing-negative-pattern-from-pattern-either)

This Semgrep rule aims to detect Python code snippets where a function `a(...)`, `b(...)`, or `c(...)` is called,
but it should not match the case where function `a()` is called with the argument `x`.
See this
[pattern\-not\-with\-pattern\-either example](https://semgrep.dev/s/5N96)


```
 1rules:
 2- id: pattern-not-in-pattern-either
 3  patterns:
 4    - pattern-either:
 5       - pattern: a(...)
 6       - pattern: b(...)
 7       - pattern: c(...)
 8    - pattern-not: a(x)
 9  message: pattern either with one negative pattern
10  languages: [python]
11  severity: WARNING

```
### Maintaining good quality of Semgrep rules
[\#](#maintaining-good-quality-of-semgrep-rules)

Before publishing a new rule or updating an existing one, it is crucial to ensure that it meets specific standards and
is effective.
To help with this, we’ve created a
[Development Practices checklist](https://github.com/trailofbits/semgrep-rules/blob/main/CONTRIBUTING.md#development-practices)
in our *Contributing to Trail of Bits Semgrep Rules* document that you can follow to make sure your custom rule
is ready for publication.

### Help with writing custom rules
[\#](#help-with-writing-custom-rules)


> **Warning:** Be careful about asking for external assistance for writing rules or sharing rule output
> that may be specific to a sensitive and/or private codebase. Doing so could inadvertently disclose the identity
> of the code owner, portions of the code, or particular bugs.

When running into issues while working on custom rules, several resources are available to help you.
Two of the most valuable resources are the following:

* The
[Semgrep Community Slack](https://go.semgrep.dev/slack) is a great place to ask for help with custom rule
development. The channel is staffed by knowledgeable developers familiar with Semgrep’s architecture and syntax.
They are usually quick to respond to questions. They can guide you in structuring your rules and in debugging any issues
that arise. Additionally, the Slack channel is a great place to connect with other developers working on similar
projects, allowing you to learn from others’ experiences and share your insights.
* Use
[Semgrep GitHub issues](https://github.com/returntocorp/semgrep/issues) to report bugs, suggest new features, and
ask for help with specific issues.

Thoroughly testing Semgrep rules for optimal performance
[\#](#thoroughly-testing-semgrep-rules-for-optimal-performance)
------------------------------------------------------------------------------------------------------------------------

Creating comprehensive tests for your Semgrep rules is essential to ensure they perform as expected and cover a wide range
of test cases. By thoroughly testing the rules against various code samples, you can confirm that they accurately identify
intended vulnerabilities, potential errors, or coding standard violations. This ultimately leads to more reliable
and effective security and code quality analysis.

### Designing comprehensive test cases
[\#](#designing-comprehensive-test-cases)

A well\-rounded test suite for a custom Semgrep rule should cover multiple aspects of the rule’s functionality.

When designing test cases, consider the following:

1. **Create a file containing code samples**: Create a file containing code with the same name as the rule.
For example, if your rule filename is `unsafe-exec.yml`, create a corresponding `unsafe-exec.py` file with sample code.
2. **Incorporate a diverse range of code samples**: Adhere to the following guidelines when adding code samples to the
test file:
	* Include at least one true positive comment (e.g., `// ruleid: id-of-your-rule`).
	* Include at least one true negative comment (e.g., `// ok: id-of-your-rule`).
	* Start with simple, descriptive examples that are easy to understand.
	* Progress to more advanced, complex examples, such as those involving nested structures (e.g., inside an `if` statement)
	or deep expressions.
	* Include edge cases that may challenge the rule’s accuracy or efficiency, such as large input values, complex code
	structures, or unusual data types.
	* Test the rule against different language features and constructs, including loops, conditionals, classes, and functions.
	* Intentionally create code samples that should not trigger the rule, and ensure that the rule does not produce
	false positives in these cases.
3. **Ensure all tests pass**: Run the `$ semgrep --test` command to verify that all test cases pass.
4. **Evaluate the rule against real\-world code**: Test the rule against actual code from your projects,
open\-source repositories, or other codebases to assess its effectiveness in real\-life scenarios.

Autofix feature
[\#](#autofix-feature)
--------------------------------------

The autofix feature can automatically correct identified vulnerabilities, potential errors, or coding standard violations.

There are many benefits to using the autofix feature:

* Training every developer on all the best practices for large code bases is not feasible. Autofixes can help fill in
the gaps and provide guidance as needed.
* Autofixes maintain developer focus by removing monotonous changes, allowing them to concentrate on more complex tasks.
* Adding autofixes allows developers to be educated and trained on new best practices as they are introduced into the codebase.
* Autofixes can provide on\-demand fixes and are much more actionable and educational than simple lint warnings.
* Without making developers aware of a deprecation, they won’t know not to use a deprecated component,
and they won’t know what to use instead. Autofixes can help make these transitions smoother.

### Creating a Semgrep rule with the autofix feature
[\#](#creating-a-semgrep-rule-with-the-autofix-feature)

Follow these steps to develop a rule with the autofix feature (see the
[ioutil\-readdir\-deprecated](https://semgrep.dev/s/wPEX)
rule with the autofix feature implemented):

1. Add the `fix` key to a rule, specifying the replacement pattern for the identified vulnerability.

Here is an example rule with the autofix feature:


```
1rules:
2  - id: ioutil-readdir-deprecated
3    languages: [golang]
4    message: ioutil.ReadDir is deprecated. Use more efficient os.ReadDir.
5    severity: WARNING
6    pattern: ioutil.ReadDir($X)
7    fix: os.ReadDir($X)

```
For the following Golang code:


```
 1package main
 2
 3import (
 4  "fmt"
 5  "io/ioutil"
 6  "log"
 7  "os"
 8)
 9
10func main() {
11    // ruleid: ioutil-readdir-deprecated
12  files, err := ioutil.ReadDir(".")
13  if err != nil {
14    log.Fatal(err)
15  }
16
17  for _, file := range files {
18    fmt.Println(file.Name())
19  }
20}

```
2. Run the rule using the standard command to confirm that the rule is detecting the intended issue:


```
$ semgrep -f rule.yaml
# (...)
Findings:

  readdir.go
    ioutil-readdir-deprecated
        ioutil.ReadDir is deprecated. Use more efficient os.ReadDir.

        ▶▶┆ Autofix ▶ os.ReadDir(".")
        11┆ files, err := ioutil.ReadDir(".")
# (...)

```
3. Run the rule with the `--dryrun` and the `--autofix` options to preview the behavior of the autofix feature on the code
without making any changes to the analyzed code:


```
$ semgrep -f rule.yaml --dryrun --autofix
# (...)
Findings:

  readdir.go
    ioutil-readdir-deprecated
        ioutil.ReadDir is deprecated. Use more efficient os.ReadDir.

        ▶▶┆ Autofix ▶ os.ReadDir(".")
        11┆ files, err := os.ReadDir(".")
# (...)

```
4. Create a new test file for the autofix by adding the `.fixed` suffix in front of the file extension
(e.g., `readdir.go` \-\> `readdir.fixed.go`). This file should contain the expected output after the autofix is applied.

Content of the `readdir.fixed.go` file:


```
 1package main
 2
 3import (
 4  "fmt"
 5  "io/ioutil"
 6  "log"
 7  "os"
 8)
 9
10func main() {
11    // ruleid: ioutil-readdir-deprecated
12  files, err := os.ReadDir(".")
13  if err != nil {
14    log.Fatal(err)
15  }
16
17  for _, file := range files {
18    fmt.Println(file.Name())
19  }
20}

```
5. Run the test to confirm that the autofix is working as expected:


```
$ semgrep --test
1/1: ✓ All tests passed
1/1: ✓ All fix tests passed

```
6. Now you are ready to apply autofix to the analyzed file with the `--autofix` option.


```
$ semgrep -f rule.yaml --autofix
# (...)
Findings:

  readdir.go
    ioutil-readdir-deprecated
        ioutil.ReadDir is deprecated. Use more efficient os.ReadDir.

        ▶▶┆ Autofix ▶ os.ReadDir(".")
        11┆ files, err := ioutil.ReadDir(".")
# (...)

```

By following these steps, you can create a custom Semgrep rule with an effective autofix feature that identifies issues
and provides a solution to fix them.

### Regular expression\-based autofix
[\#](#regular-expression-based-autofix)

The `fix` field presented above allows you to specify a simple string replacement, while the `fix-regex` field enables
more complex regular expression\-based replacements. For more information, refer to the official documentation
on
[Autofix with regular expression replacement](https://semgrep.dev/docs/writing-rules/autofix/#autofix-with-regular-expression-replacement).

Optimizing Semgrep rules
[\#](#optimizing-semgrep-rules)
--------------------------------------------------------


> Improve rule performance and minimize false positives through repeatable processes.

Optimizing your Semgrep rules is crucial for maintaining high performance and minimizing false positives.
This section will guide how to create efficient and accurate Semgrep rules.

1. **Analyze time summary**: To include a time summary with the results, use the `--time` flag. This will provide the
following information:


	* Total time / Config time / Core time
	* Semgrep\-core time
		+ Total CPU time
		+ File parse time
		+ Rule parse time
		+ Matching time
	* Slowest five analyzed files
	* Slowest five rules to match
2. **Narrow down findings to specific file paths**: Assess whether findings should be limited to specific file paths
(e.g., Dockerfiles).


	* You can apply particular rules to certain paths using the `paths` keyword. For example, the
	[avoid\-apt\-get\-upgrade](https://semgrep.dev/playground/r/generic.dockerfile.best-practice.avoid-apt-get-upgrade.avoid-apt-get-upgrade)
	rule targets only Dockerfiles:
	
	
	```
	17  paths:
	18      include:
	19        - "*dockerfile*"
	20        - "*Dockerfile*"
	
	```
3. **Use `pattern-inside` and `pattern-not-inside`**: The `pattern-inside` and `pattern-not-inside` clauses allow you to
specify a context in which a pattern should or should not be matched, respectively.

Consider a scenario where you want to identify calls to `insecure_function()` within a loop,
followed by a specific statement, such as a call to `log_data()`, but only when the log level is set to `DEBUG`.

Initially, you can achieve this by using one `pattern` statement:


```
 1rules:
 2- id: insecure_function_in_loop_followed_by_debug_log
 3  languages: [python]
 4  message: |
 5    Insecure function called within a loop
 6    followed by log_data() with log level DEBUG    
 7  severity: WARNING
 8  pattern: |
 9    for ... in ...:
10        ...
11        insecure_function(...)
12        ...
13        log_data("DEBUG", ...)    

```
Here’s an example of Python code that triggers the `insecure_function_in_loop_followed_by_debug_log` rule:


```
 1def insecure_function():
 2    print("Insecure function called")
 3
 4def log_data(log_level, msg):
 5    if log_level == "DEBUG":
 6        print("DEBUG:", msg)
 7
 8def main():
 9    data_list = ['data1', 'data2', 'data3']
10
11for data in data_list:
12    # Call to insecure_function() within a loop,
13    # followed by log_data() with log level DEBUG triggers the rule
14    insecure_function()
15    other_function()
16    function1337()
17    log_data("DEBUG", "Insecure function called with data: " + data)

```
Running the `insecure_function_in_loop_followed_by_debug_log` rule may not provide the clearest output,
as it displays the entire `for` loop:


```
$ semgrep -f insecure_function_in_loop_followed_by_debug_log.yml
# (...)
  insecure_function_in_loop_followed_by_debug_log
    Insecure function called within a loop followed by log_data() with log level DEBUG

    11┆ for data in data_list:
    12┆  # Call to insecure_function() within a loop,
    13┆  # followed by log_data() with log level DEBUG triggers the rule
    14┆  insecure_function()
    15┆  other_function()
    16┆  function1337()
    17┆  log_data("DEBUG", "Insecure function called with data: " + data)

```
For such findings, only the calls to `insecure_function()` might be of critical importance. To improve the output,
you can use the following clauses instead:


	1. `patterns`: This clause combines two sub\-patterns with a logical AND operator, meaning all sub\-patterns
	must match:
	
	a. `pattern-inside`: This clause matches any `for` loop in the Python code, establishing the context for
	the subsequent patterns. It sets a condition that must be met for the rule to trigger, acting
	as the first part of a logical AND operation.
	
	b. `pattern`: This sub\-pattern matches calls to any function followed by a call to `log_data("DEBUG", ...)`.
	The rule potentially triggers if this `pattern` and the previous `pattern-inside` match.
	
	c. `focus-metavariable`: This operator focuses the finding on the line of code matched by `$FUNC`.
	
	d. `metavariable-pattern`: This sub\-pattern restricts `$FUNC` to functions called `insecure_function`.Here is a fixed version of the `insecure_function_in_loop_followed_by_debug_log` rule:


```
 1rules:
 2- id: insecure_function_in_loop_followed_by_debug_log_fixed
 3  languages: [python]
 4  message: |
 5    Insecure function called within a loop
 6    followed by log_data() with log level DEBUG    
 7  severity: WARNING
 8  patterns:
 9    - pattern-inside: |
10        for ... in ...:
11            ...        
12    - pattern: |
13        $FUNC(...)
14        ...
15        log_data("DEBUG", ...)        
16    - focus-metavariable: $FUNC
17    - metavariable-pattern:
18        metavariable: $FUNC
19        pattern: insecure_function

```
Running the `insecure_function_in_loop_followed_by_debug_log_fixed` Semgrep rule will produce a more concise and
focused output:


```
$ semgrep -f insecure_function_in_loop_followed_by_debug_log_fixed.yml
# (...)
  insecure_function_in_loop_followed_by_debug_log_fixed
      Insecure function called within a loop followed by log_data() with log level DEBUG

      13┆ insecure_function()

```
4. **Minimize the use of ellipses** `...`: While ellipses are a powerful tool for matching a wide range of code snippets,
they can lead to performance issues and false positives when overused. Limit the use of ellipses to situations necessary
for accurate pattern matching.
5. **Determine the necessity of metavariables**: Before using a metavariable in your rule, determine if it is truly necessary.
Metavariables can be useful for capturing and comparing values, but if a metavariable is unnecessary for your rule
to function correctly, consider removing it.

For example, consider the following Semgrep rule that uses a metavariable `$X`:


```
1rules:
2  - id: unnecessary_metavariable_example
3    languages: [python]
4    message: The variable is assigned the value 123
5    pattern: $X = 123
6    severity: WARNING

```
This rule matches any variable assignment with the value `123`. However, the metavariable `$X` might be unnecessary
if you don’t need to capture the variable name. In this case, you can use the `...` operator instead, which matches any
expression:


```
1rules:
2  - id: without_metavariable_example
3    languages: [python]
4    message: A variable is assigned the value 123
5    pattern: ... = 123
6    severity: WARNING

```
By replacing the `$X` metavariable with the `...` operator, you can reduce the complexity and improve the performance
of your rule without losing the intended functionality. This approach should be used when the metavariable is not essential
for the rule’s purpose or subsequent comparisons or checks.
6. **Test your rules with real\-world code**: To ensure the effectiveness of your rules, test them with real\-world code samples.
This lets you identify potential issues and false positives before deploying your rules in a production environment.
[![Edit](Advanced%20usage%20_%20Testing%20Handbook_files/edit.svg)
Edit this page](https://github.com/trailofbits/testing-handbook/edit/main/content/docs/static-analysis/semgrep/10-advanced.md)\|
[Trail of Bits](https://www.trailofbits.com/)
\|
[Trail of Bits Blog](https://blog.trailofbits.com/)
\|
[Contact us](https://www.trailofbits.com/contact/)This content is licensed under a
[Creative Commons Attribution 4\.0 International license.](https://creativecommons.org/licenses/by/4.0/)* [Ignoring (parts of) code in your project with Semgrep](#ignoring-parts-of-code-in-your-project-with-semgrep)
	+ [Files/directories](#filesdirectories)
	+ [Excluding code sections](#excluding-code-sections)
* [Writing custom rules](#writing-custom-rules)
	+ [Example custom rule](#example-custom-rule)
	+ [Running custom rules](#running-custom-rules)
	+ [ABCs of writing custom rules](#abcs-of-writing-custom-rules)
	+ [Building blocks](#building-blocks)
	+ [Combining patterns](#combining-patterns)
	+ [Generic pattern matching](#generic-pattern-matching)
	+ [Metadata](#metadata)
	+ [Various tips](#various-tips)
	+ [Maintaining good quality of Semgrep rules](#maintaining-good-quality-of-semgrep-rules)
	+ [Help with writing custom rules](#help-with-writing-custom-rules)
* [Thoroughly testing Semgrep rules for optimal performance](#thoroughly-testing-semgrep-rules-for-optimal-performance)
	+ [Designing comprehensive test cases](#designing-comprehensive-test-cases)
* [Autofix feature](#autofix-feature)
	+ [Creating a Semgrep rule with the autofix feature](#creating-a-semgrep-rule-with-the-autofix-feature)
	+ [Regular expression\-based autofix](#regular-expression-based-autofix)
* [Optimizing Semgrep rules](#optimizing-semgrep-rules)










Pattern syntax \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Pattern%20syntax%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* Pattern syntax
On this page* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Pattern syntax
==============


tipGetting started with rule writing? Try the [Semgrep Tutorial](https://semgrep.dev/learn) 🎓


This document describes Semgrep’s pattern syntax. You can also see pattern [examples by language](https://semgrep.dev/docs/writing-rules/pattern-examples). In the command line, patterns are specified with the flag `--pattern` (or `-e`). Multiple
coordinating patterns may be specified in a configuration file. See
[rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax) for more information.


Pattern matching[​](#pattern-matching "Direct link to Pattern matching")
------------------------------------------------------------------------


Pattern matching searches code for a given pattern. For example, the
expression pattern `1 + func(42)` can match a full expression or be
part of a subexpression:



```
foo(1 + func(42)) + bar()  

```

In the same way, the statement pattern `return 42` can match a top
statement in a function or any nested statement:



```
def foo(x):  
  if x > 1:  
     if x > 2:  
       return 42  
  return 42  

```

Ellipsis operator[​](#ellipsis-operator "Direct link to Ellipsis operator")
---------------------------------------------------------------------------


The `...` ellipsis operator abstracts away a sequence of zero or more
items such as arguments, statements, parameters, fields, characters.


The `...` ellipsis can also match any single item that is not part of
a sequence when the context allows it.


See the use cases in the subsections below.


### Function calls[​](#function-calls "Direct link to Function calls")


Use the ellipsis operator to search for function calls or
function calls with specific arguments. For example, the pattern `insecure_function(...)` finds calls regardless of its arguments.



```
insecure_function("MALICIOUS_STRING", arg1, arg2)  

```

Functions and classes can be referenced by their fully qualified name, e.g.,


* `django.utils.safestring.mark_safe(...)` or `mark_safe(...)`
* `System.out.println(...)` or `println(...)`


You can also search for calls with arguments after a match. The pattern `func(1, ...)` will match both:



```
func(1, "extra stuff", False)  
func(1)  # Matches no arguments as well  

```

Or find calls with arguments before a match with `func(..., 1)`:



```
func("extra stuff", False, 1)  
func(1)  # Matches no arguments as well  

```

The pattern `requests.get(..., verify=False, ...)` finds calls where an argument appears anywhere:



```
requests.get(verify=False, url=URL)  
requests.get(URL, verify=False, timeout=3)  
requests.get(URL, verify=False)  

```

Match the keyword argument value with the pattern `$FUNC(..., $KEY=$VALUE, ...)`.


### Method calls[​](#method-calls "Direct link to Method calls")


The ellipsis operator can also be used to search for method calls.
For example, the pattern `$OBJECT.extractall(...)` matches:



```
tarball.extractall('/path/to/directory')  # Oops, potential arbitrary file overwrite  

```

You can also use the ellipsis in chains of method calls. For example,
the pattern `$O.foo(). ... .bar()` will match:



```
obj = MakeObject()  
obj.foo().other_method(1,2).again(3,4).bar()  
  

```

### Function definitions[​](#function-definitions "Direct link to Function definitions")


The ellipsis operator can be used in function parameter lists or in the function
body. To find function definitions with [mutable default arguments](https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments):



```
pattern: |  
  def $FUNC(..., $ARG={}, ...):  
      ...  

```


```
def parse_data(parser, data={}):  # Oops, mutable default arguments  
    pass  

```

tipThe YAML `|` operator allows for [multiline strings](https://yaml-multiline.info/).


The ellipsis operator can match the function name.
Match any function definition:
Regular functions, methods, and also anonymous functions (such as lambdas).
To match named or anonymous functions use an ellipsis `...` in place of the name of the function.
For example, in JavaScript the pattern `function ...($X) { ... }` matches
any function with one parameter:



```
function foo(a) {  
  return a;  
}  
var bar = function (a) {  
  return a;  
};  

```

### Class definitions[​](#class-definitions "Direct link to Class definitions")


The ellipsis operator can be used in class definitions. To find classes that
inherit from a certain parent:



```
pattern: |  
  class $CLASS(InsecureBaseClass):  
      ...  

```


```
class DataRetriever(InsecureBaseClass):  
    def __init__(self):  
        pass  

```

tipThe YAML `|` operator allows for [multiline strings](https://yaml-multiline.info/).


#### Ellipsis operator scope[​](#ellipsis-operator-scope "Direct link to Ellipsis operator scope")


The `...` ellipsis operator matches everything in its 
current scope. The current scope of this operator is defined by the 
patterns that precede `...` in a rule. See the following example:



Semgrep matches the first occurrence of `bar` and `baz` in the test code as these objects fall under the scope of `foo` and `...`. The ellipsis operator does not match the second occurrence of `bar` and `baz`
 as they are not inside of the function definition, therefore these 
objects in their second occurrence are not inside the scope of the 
ellipsis operator.


### Strings[​](#strings "Direct link to Strings")


The ellipsis operator can be used to search for strings containing any data. The pattern `crypto.set_secret_key("...")` matches:



```
crypto.set_secret_key("HARDCODED SECRET")  

```

This also works with [constant propagation](#constants).


In languages where regular expressions use a special syntax
(for example JavaScript), the pattern `/.../` will match
any regular expression construct:



```
re1 = /foo|bar/;  
re2 = /a.*b/;  

```

### Binary operations[​](#binary-operations "Direct link to Binary operations")


The ellipsis operator can match any number of arguments to binary operations. The pattern `$X = 1 + 2 + ...` matches:



```
foo = 1 + 2 + 3 + 4  

```

### Containers[​](#containers "Direct link to Containers")


The ellipsis operator can match inside container data structures like lists, arrays, and key\-value stores.


The pattern `user_list = [..., 10]` matches:



```
user_list = [8, 9, 10]  

```

The pattern `user_dict = {...}` matches:



```
user_dict = {'username': 'password'}  

```

The pattern `user_dict = {..., $KEY: $VALUE, ...}` matches the following and allows for further metavariable queries:



```
user_dict = {'username': 'password', 'address': 'zipcode'}  

```

You can also match just a key\-value pair in
a container, for example in JSON the pattern `"foo": $X` matches
just a single line in:



```
{ "bar": True,  
  "name": "self",  
  "foo": 42  
}  

```

### Conditionals and loops[​](#conditionals-and-loops "Direct link to Conditionals and loops")


The ellipsis operator can be used inside conditionals or loops. The pattern:



```
pattern: |  
  if $CONDITION:  
      ...  

```

tipThe YAML `|` operator allows for [multiline strings](https://yaml-multiline.info/).


matches:



```
if can_make_request:  
    check_status()  
    make_request()  
    return  

```

A metavariable can match a conditional or loop body if the body statement information is re\-used later. The pattern:



```
pattern: |  
  if $CONDITION:  
      $BODY  

```

matches:



```
if can_make_request:  
    single_request_statement()  

```

tipHalf
 or partial statements can't be matches; both of the examples above must
 specify the contents of the condition’s body (e.g., `$BODY` or `...`), otherwise they are not valid patterns.


### Matching single items with an ellipsis[​](#matching-single-items-with-an-ellipsis "Direct link to Matching single items with an ellipsis")


Ellipsis `...` is generally used to match sequences of similar elements.
However, you can also match single item using ellipsis `...` operator.
The following pattern is valid in languages with a C\-like
syntax even though `...` matches a single Boolean value rather
than a sequence:



```
if (...)  
  return 42;  

```

Another example where a single expression is matched by an ellipsis is
the right\-hand side of assignments:



```
foo = ...;  

```

However, matching a sequence of items remains the default meaning of an
ellipsis. For example, the pattern `bar(...)` matches `bar(a)`,
but also `bar(a, b)` and `bar()`. To force a match on a single item,
use a metavariable as in `bar($X)`.


Metavariables[​](#metavariables "Direct link to Metavariables")
---------------------------------------------------------------


Metavariables are an abstraction to match code when you don’t know the value or contents ahead of time, similar to [capture groups](https://regexone.com/lesson/capturing_groups) in regular expressions.


Metavariables can be used to track values across a specific code scope. This
includes variables, functions, arguments, classes, object methods, imports,
exceptions, and more.


Metavariables look like `$X`, `$WIDGET`, or `$USERS_2`. They begin with a `$` and can only
contain uppercase characters, `_`, or digits. Names like `$x` or `$some_value` are invalid.


### Expression metavariables[​](#expression-metavariables "Direct link to Expression metavariables")


The pattern `$X + $Y` matches the following code examples:



```
foo() + bar()  

```


```
current + total  

```

### Import metavariables[​](#import-metavariables "Direct link to Import metavariables")


Metavariables can also be used to match imports. For example, `import $X` matches:



```
import random  

```

### Reoccurring metavariables[​](#reoccurring-metavariables "Direct link to Reoccurring metavariables")


Re\-using metavariables shows their true power. Detect useless assignments:



```
pattern: |  
  $X = $Y  
  $X = $Z  

```

Useless assignment detected:



```
initial_value = 10  # Oops, useless assignment  
initial_value = get_initial_value()  

```

tipThe YAML `|` operator allows for [multiline strings](https://yaml-multiline.info/).


### Literal Metavariables[​](#literal-metavariables "Direct link to Literal Metavariables")


You can use `"$X"` to match any string literal. This is similar
to using `"..."`, but the content of the string is stored in the
metavariable `$X`, which can then be used in a message
or in a [`metavariable-regex`](https://semgrep.dev/docs/writing-rules/rule-syntax#metavariable-regex).


You can also use `/$X/` and `:$X` to respectively match
any regular expressions or atoms (in languages that support
those constructs, e.g., Ruby).


### Typed metavariables[​](#typed-metavariables "Direct link to Typed metavariables")


#### Syntax[​](#syntax "Direct link to Syntax")


Typed metavariables only match a metavariable if it’s declared as a specific type.


##### Java:[​](#java "Direct link to Java:")


For example, to look for calls to the `log` method on `Logger` objects.
A simple pattern for this purpose could use a metavariable for the Logger object.



```
pattern: $LOGGER.log(...)  

```

But if we are concerned about finding calls to the `Math.log()` method as well, we can use a typed metavariable to put a type constraint on the `$LOGGER` metavariable.



```
pattern: (java.util.logging.Logger $LOGGER).log(...)  

```

Alternatively, if we want to capture more logger types, for example 
custom logger types, we could instead add a constraint to the type of 
the argument in this method call instead.



```
pattern: $LOGGER.log(java.util.logging.LogRecord $RECORD)  

```

##### C:[​](#c "Direct link to C:")


In this example in C, we want to capture all cases where something is compared to a char array.
We start with a simple pattern that looks for comparison between two variables.



```
pattern: $X == $Y  

```

We can then put a type constraint on one of the metavariables used in this pattern by turning it into a typed metavariable.



```
pattern: $X == (char *$Y)  

```


```
int main() {  
    char *a = "Hello";  
    int b = 1;  
  
    // Matched  
    if (a == "world") {  
        return 1;  
    }  
  
    // Not matched  
    if (b == 2) {  
        return -1;  
    }  
  
    return 0;  
}  

```

##### Go:[​](#go "Direct link to Go:")


The syntax for a typed metavariable in Go looks different from the syntax for Java.
In this Go example we look for calls to the `Open` function, but only on an object of the `zip.Reader` type.



```
pattern: ($READER : *zip.Reader).Open($INPUT)  

```


```
func read_file() {  
  
    reader, _ := zip.NewReader(readerat, 18276)  
  
	// Matched  
	reader.Open("data")  
  
    dir := http.Dir("/")  
  
	// Not matched  
	f, err := dir.Open(c.Param("file"))  
}  

```

cautionFor
 Go, Semgrep currently does not recognize the type of all variables that
 are declared on the same line. That is, the following will not take 
both `a` and `b` as `int`s: `var a, b = 1, 2`


##### TypeScript:[​](#typescript "Direct link to TypeScript:")


In this example, we want to look for uses of the DomSanitizer function.



```
pattern: ($X: DomSanitizer).sanitize(...)  

```


```
constructor(  
  private _activatedRoute: ActivatedRoute,  
  private sanitizer: DomSanitizer,  
) { }  
  
ngOnInit() {  
    // Not matched  
    this.sanitizer.bypassSecurityTrustHtml(DOMPurify.sanitize(this._activatedRoute.snapshot.queryParams['q']))  
  
    // Matched  
    this.sanitizer.bypassSecurityTrustHtml(this.sanitizer.sanitize(this._activatedRoute.snapshot.queryParams['q']))  
}  

```

#### Using typed metavariables[​](#using-typed-metavariables "Direct link to Using typed metavariables")


Type inference applies to the entire file! One common way to use 
typed metavariables is to check for a function called on a specific type
 of object. For example, let's say you're looking for calls to a 
potentially unsafe logger in a class like this:



```
class Test {  
    static Logger logger;  
  
    public static void run_test(String input, int num) {  
        logger.log("Running a test with " + input);  
  
        test(input, Math.log(num));  
    }  
}  

```

If you searched for `$X.log(...)`, you can also match `Math.log(num)`. Instead, you can search for `(Logger $X).log(...)` which gives you the call to `logger`. See the rule [`logger_search`](https://semgrep.dev/playground/s/lgAo).


cautionSince
 matching happens within a single file, this is only guaranteed to work 
for local variables and arguments. Additionally, Semgrep currently 
understands types on a shallow level. For example, if you have `int[] A`, it will not recognize `A[0]`
 as an integer. If you have a class with fields, you will not be able to
 use typechecking on field accesses, and it will not recognize the 
class’s field as the expected type. Literal types are understood to a 
limited extent. Expanded type support is under active development.


### Ellipsis metavariables[​](#ellipsis-metavariables "Direct link to Ellipsis metavariables")


You can combine ellipses and metavariables to match a sequence
of arguments and store the matched sequence in a metavariable.
For example the pattern `foo($...ARGS, 3, $...ARGS)` will
match:



```
foo(1,2,3,1,2)  

```

When referencing an ellipsis metavariable in a rule message or [metavariable\-pattern](https://semgrep.dev/docs/writing-rules/rule-syntax#metavariable-pattern), include the ellipsis:



```
- message: Call to foo($...ARGS)  

```

### Anonymous metavariables[​](#anonymous-metavariables "Direct link to Anonymous metavariables")


Anonymous metavariables are used to specify that a metavariable exists in the pattern you want to capture.


An anonymous metavariable always takes the form `$_`. Variables such as `$_1` or `$_2` are **not** anonymous. You can use more than one anonymous metavariable in a rule definition.


For example, if you want to specify that a function should **always** have 3 arguments, then you can use anonymous metavariables:



```
- pattern: def function($_, $_, $_)  

```

An anonymous metavariable does not produce any binding to the code it
 matched. This means it does not enforce that it matches the same code 
at each place it is used. The pattern:



```
- pattern: def function($A, $B, $C)  

```

is not equivalent to the former example, as `$A`, `$B`, and `$C` bind to the code that matched the pattern. You can then use `$A`
 or any other metavariable in your rule definition to specify that 
specific code. Anonymous metavariables cannot be used this way.


Anonymous metavariables also communicate to the reader that their 
values are not relevant, but rather their occurrence in the pattern.


### Metavariable unification[​](#metavariable-unification "Direct link to Metavariable unification")


For search mode rules, metavariables with the same name are treated as the same metavariable within the `patterns` operator. This is called metavariable unification.


For taint mode rules, patterns defined **within** `pattern-sinks` and `pattern-sources` still unify. However, metavariable unification **between** `pattern-sinks` and `pattern-sources` is **not** enabled by default.


To enforce unification, set `taint_unify_mvars: true` under the rule `options` key. When `taint_unify_mvars: true` is set, a metavariable defined in `pattern-sinks` and `pattern-sources` with the same name is treated as the same metavariable. See [Metavariables, rule message, and unification](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode#metavariables-rule-message-and-unification) for more information.


### Display matched metavariables in rule messages[​](#display-matched-metavariables-in-rule-messages "Direct link to Display matched metavariables in rule messages")


Display values of matched metavariables in rule messages. Add a metavariable to the rule message (for example `Found $X`) and Semgrep replaces it with the value of the detected metavariable.


To display matched metavariable in a rule message, add the same 
metavariable as you are searching for in your rule to the rule message.


1. Find the metavariable used in the Semgrep rule. See the following example of a part Semgrep rule (formula):

```
- pattern: $MODEL.set_password(…)  

```

This formula uses `$MODEL` as a metavariable.
2. Insert the metavariable to rule message:

```
- message: Setting a password on $MODEL  

```
3. Use the formula displayed above against the following code:

```
user.set_password(new_password)  

```


The resulting message is:



```
Setting a password on user  

```

Run the following example in Semgrep Playground to see the message (click **Open in Editor**, and then **Run**, unroll the **1 Match** to see the message):



infoIf you're using Semgrep's advanced dataflow features, see documentation of experimental feature [Displaying propagated value of metavariable](https://semgrep.dev/docs/writing-rules/experiments/display-propagated-metavariable).


Equivalences[​](#equivalences "Direct link to Equivalences")
------------------------------------------------------------


Semgrep automatically searches for code that is semantically equivalent.


### Imports[​](#imports "Direct link to Imports")


Equivalent imports using aliasing or submodules are matched.


The pattern `subprocess.Popen(...)` matches:



```
import subprocess.Popen as sub_popen  
sub_popen('ls')  

```

The pattern `foo.bar.baz.qux(...)` matches:



```
from foo.bar import baz  
baz.qux()  

```

### Constants[​](#constants "Direct link to Constants")


Semgrep performs constant propagation.


The pattern `set_password("password")` matches:



```
HARDCODED_PASSWORD = "password"  
  
def update_system():  
    set_password(HARDCODED_PASSWORD)  

```

Basic constant propagation support like in the example above is a stable feature.
Experimentally, Semgrep also supports [intra\-procedural flow\-sensitive constant propagation](https://semgrep.dev/docs/writing-rules/data-flow/constant-propagation).


The pattern `set_password("...")` also matches:



```
def update_system():  
    if cond():  
        password = "abc"  
    else:  
        password = "123"  
    set_password(password)  

```

tipIt is possible to disable constant propagation in a per\-rule basis via the [`options` rule field](https://semgrep.dev/docs/writing-rules/rule-syntax#options).


### Associative and commutative operators[​](#associative-and-commutative-operators "Direct link to Associative and commutative operators")


Semgrep performs associative\-commutative (AC) matching. For example, `... && B && C` will match both `B && C` and `(A && B) && C` (i.e., `&&` is associative). Also, `A | B | C` will match `A | B | C`, and `B | C | A`, and `C | B | A`, and any other permutation (i.e., `|` is associative and commutative).


Under AC\-matching metavariables behave similarly to `...`. For example, `A | $X` can match `A | B | C` in four different ways (`$X` can bind to `B`, or `C`, or `B | C`).
 In order to avoid a combinatorial explosion, Semgrep will only perform 
AC\-matching with metavariables if the number of potential matches is *small*, otherwise it will produce just one match (if possible) where each metavariable is bound to a single operand.


Using [`options`](https://semgrep.dev/docs/writing-rules/rule-syntax#options) it is possible to entirely disable AC\-matching. It is also possible to treat Boolean AND and OR operators (e.g., `&&` in `||` in C\-family languages) as commutative, which can be useful despite not being semantically accurate.


Deep expression operator[​](#deep-expression-operator "Direct link to Deep expression operator")
------------------------------------------------------------------------------------------------


Use the deep expression operator `<... [your_pattern] ...>`
 to match an expression that could be deeply nested within another 
expression. An example is looking for a pattern anywhere within an `if`
 statement. The deep expression operator matches your pattern in the 
current expression context and recursively in any subexpressions.


For example, this pattern:



```
pattern: |  
  if <... $USER.is_admin() ...>:  
    ...  

```

matches:



```
if user.authenticated() and user.is_admin() and user.has_group(gid):  
  [ CONDITIONAL BODY ]  

```

The deep expression operator works in:


* `if` statements: `if <... $X ...>:`
* nested calls: `sql.query(<... $X ...>)`
* operands of a binary expression: `"..." + <... $X ...>`
* any other expression context


Limitations[​](#limitations "Direct link to Limitations")
---------------------------------------------------------


### Statements types[​](#statements-types "Direct link to Statements types")


Semgrep handles some statement types differently than others, 
particularly when searching for fragments inside statements. For 
example, the pattern `foo` will match these statements:



```
x += foo()  
return bar + foo  
foo(1, 2)  

```

But `foo` will not match the following statement (`import foo` will match it though):



```
import foo  

```

#### Statements as expressions[​](#statements-as-expressions "Direct link to Statements as expressions")


Many programming languages differentiate between expressions and 
statements. Expressions can appear inside if conditions, in function 
call arguments, etc. Statements can not appear everywhere; they are 
sequence of operations (in many languages using `;` as a separator/terminator) or special control flow constructs (if, while, etc.).


`foo()` is an expression (in most languages).


`foo();` is a statement (in most languages).


If your search pattern is a statement, Semgrep will automatically try to search for it as *both* an expression and a statement.


When you write the expression `foo()` in a pattern, Semgrep will visit every expression and sub\-expression in your program and try to find a match.


Many programmers don't really see the difference between `foo()` and `foo();`. This is why when one looks for `foo()`; Semgrep thinks the user wants to match statements like `a = foo();`, or `print(foo());`.


infoNote
 that in some programming languages such as Python, which does not use 
semicolons as a separator or terminator, the difference between 
expressions and statements is even more confusing. Indentation in Python
 matters, and a newline after `foo()` is really the same than `foo();` in other programming languages such as C.


### Partial expressions[​](#partial-expressions "Direct link to Partial expressions")


Partial expressions are not valid patterns. For example, the following is invalid:



```
pattern: 1+  

```

A complete expression is needed (like `1 + $X`)


### Ellipses and statement blocks[​](#ellipses-and-statement-blocks "Direct link to Ellipses and statement blocks")


The [ellipsis operator](#ellipsis-operator) does *not* jump from inner to outer statement blocks.


For example, this pattern:



```
foo()  
...  
bar()  

```

matches:



```
foo()  
baz()  
bar()  

```

and also matches:



```
foo()  
baz()  
if cond:  
    bar()  

```

but it does *not* match:



```
if cond:  
    foo()  
baz()  
bar()  

```

because `...` cannot jump from the inner block where `foo()` is, to the outer block where `bar()` is.


### Partial statements[​](#partial-statements "Direct link to Partial statements")


Partial statements are partially supported. For example,
you can just match the header of a conditional with `if ($E)`,
or just the try part of an exception statement with `try { ... }`.


This is especially useful when used in a
[pattern\-inside](https://semgrep.dev/docs/writing-rules/rule-syntax#pattern-inside) to restrict the
context in which to search for other things.


### Other partial constructs[​](#other-partial-constructs "Direct link to Other partial constructs")


It is possible to just match the header of a function (without its body),
for example `int foo(...)` to match just the header part of the
function `foo`. In the same way, you can just match a class header
(e.g., with `class $A`).


Deprecated features[​](#deprecated-features "Direct link to Deprecated features")
---------------------------------------------------------------------------------


### String matching[​](#string-matching "Direct link to String matching")


warningString matching has been deprecated. You should use [`metavariable-regex`](https://semgrep.dev/docs/writing-rules/rule-syntax#metavariable-regex) instead.


Search string literals within code with [Perl Compatible Regular Expressions (PCRE)](https://learnxinyminutes.com/docs/pcre/).


The pattern `requests.get("=~/dev\./i")` matches:



```
requests.get("api.dev.corp.com")  # Oops, development API left in  

```

To search for specific strings, use the syntax `"=~/<regexp>/"`. Advanced regexp features are available, such as case\-insensitive regexps with `'/i'` (e.g., `"=~/foo/i"`). Matching occurs anywhere in the string unless the regexp `^` anchor character is used: `"=~/^foo.*/"` checks if a string begins with `foo`.



---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/pattern-syntax.mdx)Last updated on **Jul 12, 2024**[PreviousPattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)[NextCustom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)* [Pattern matching](#pattern-matching)
* [Ellipsis operator](#ellipsis-operator)
	+ [Function calls](#function-calls)
	+ [Method calls](#method-calls)
	+ [Function definitions](#function-definitions)
	+ [Class definitions](#class-definitions)
	+ [Strings](#strings)
	+ [Binary operations](#binary-operations)
	+ [Containers](#containers)
	+ [Conditionals and loops](#conditionals-and-loops)
	+ [Matching single items with an ellipsis](#matching-single-items-with-an-ellipsis)
* [Metavariables](#metavariables)
	+ [Expression metavariables](#expression-metavariables)
	+ [Import metavariables](#import-metavariables)
	+ [Reoccurring metavariables](#reoccurring-metavariables)
	+ [Literal Metavariables](#literal-metavariables)
	+ [Typed metavariables](#typed-metavariables)
	+ [Ellipsis metavariables](#ellipsis-metavariables)
	+ [Anonymous metavariables](#anonymous-metavariables)
	+ [Metavariable unification](#metavariable-unification)
	+ [Display matched metavariables in rule messages](#display-matched-metavariables-in-rule-messages)
* [Equivalences](#equivalences)
	+ [Imports](#imports)
	+ [Constants](#constants)
	+ [Associative and commutative operators](#associative-and-commutative-operators)
* [Deep expression operator](#deep-expression-operator)
* [Limitations](#limitations)
	+ [Statements types](#statements-types)
	+ [Partial expressions](#partial-expressions)
	+ [Ellipses and statement blocks](#ellipses-and-statement-blocks)
	+ [Partial statements](#partial-statements)
	+ [Other partial constructs](#other-partial-constructs)
* [Deprecated features](#deprecated-features)
	+ [String matching](#string-matching)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Pattern%20syntax%20_%20Semgrep_files/adsct.gif)![](Pattern%20syntax%20_%20Semgrep_files/adsct_002.gif)
















Writing your first custom Semgrep rule \- Dock12 \- Sorint.Lab
















































[![](Writing%20your%20first%20custom%20Semgrep%20rule%20-%20Dock12%20-%20Sorint.Lab_files/SorintLAB_spa_bianco.png)](https://www.sorint.com/)















[![](Writing%20your%20first%20custom%20Semgrep%20rule%20-%20Dock12%20-%20Sorint.Lab_files/avatar.png)](https://dock12.sorint.com/)


[Dock12](https://dock12.sorint.com/)/**[Writing your first custom Semgrep rule](https://dock12.sorint.com/post/writing-your-first-custom-semgrep-rule/)**
=========================================================================================================================================================



 Created by **Luca Famà** 27 Jul 2023

 Modified 27 Jul 2023























[SAST tools and Abstract Syntax Tree](#sast-tools-and-abstract-syntax-tree)[Matching Spring unauthenticated routes using custom semgrep rule](#matching-spring-unauthenticated-routes-using-custom-semgrep-rule)[Conclusion](#conclusion)


 1809 Words
 

 

[semgrep](https://dock12.sorint.com/tags/semgrep) 
[SAST](https://dock12.sorint.com/tags/sast) 
[AST](https://dock12.sorint.com/tags/ast) 
[tree\-sitter](https://dock12.sorint.com/tags/tree-sitter) 




[Semgrep](https://semgrep.dev/) is a powerful SAST tool that performs source code analysis in order to identify vulnerabilities.


In this article we’ll see how we can write simple but effective custom semgrep rules to prevent security bugs in your code.


But let’s first introduce the Abstract Syntax Tree and why it’s related to SAST tools.


### SAST tools and Abstract Syntax Tree


SAST (Static Analysis Security Testing) is a technique that analyzes 
source code looking for vulnerable patterns. This allow us to identify 
possible security issues before deploying the application in production,
 hence reducing the risks of introducing vulnerabilities in our 
application.


SAST tools usually work on Abstract Syntax Tree (AST): the AST is a 
tree that represents the syntactic structure of the source code. It 
parses the source code and outputs a tree data structure that represents
 the actual semantic of the source code, abstracting away syntax.


For example, let’s say we have the following expression:



```
x = 1 + (y * 2)

```
We can represent it with the following (simplified) AST:


![tree](Writing%20your%20first%20custom%20Semgrep%20rule%20-%20Dock12%20-%20Sorint.Lab_files/ast-tree.png)


Of course, in real life, computers need to represent the AST in a more formal and structured way. We can use [tree\-sitter](https://tree-sitter.github.io/tree-sitter/) to see how a real AST looks like.


Let’s consider the following simple Java class:



```
public class Main {
  int x = 5;

  public static void main(String[] args) {
    Main myObj = new Main();
    System.out.println(myObj.x);
  }
}

```
And let’s parse it using `tree-sitter`. This is what we get:



```
(program [0, 0] - [8, 0]
  (class_declaration [0, 0] - [7, 1]
    (modifiers [0, 0] - [0, 6])
    name: (identifier [0, 13] - [0, 17])
    body: (class_body [0, 18] - [7, 1]
      (field_declaration [1, 2] - [1, 12]
        type: (integral_type [1, 2] - [1, 5])
        declarator: (variable_declarator [1, 6] - [1, 11]
          name: (identifier [1, 6] - [1, 7])
          value: (decimal_integer_literal [1, 10] - [1, 11])))
      (method_declaration [3, 2] - [6, 3]
        (modifiers [3, 2] - [3, 15])
        type: (void_type [3, 16] - [3, 20])
        name: (identifier [3, 21] - [3, 25])
        parameters: (formal_parameters [3, 25] - [3, 40]
          (formal_parameter [3, 26] - [3, 39]
            type: (array_type [3, 26] - [3, 34]
              element: (type_identifier [3, 26] - [3, 32])
              dimensions: (dimensions [3, 32] - [3, 34]))
            name: (identifier [3, 35] - [3, 39])))
        body: (block [3, 41] - [6, 3]
          (local_variable_declaration [4, 4] - [4, 28]
            type: (type_identifier [4, 4] - [4, 8])
            declarator: (variable_declarator [4, 9] - [4, 27]
              name: (identifier [4, 9] - [4, 14])
              value: (object_creation_expression [4, 17] - [4, 27]
                type: (type_identifier [4, 21] - [4, 25])
                arguments: (argument_list [4, 25] - [4, 27]))))
          (expression_statement [5, 4] - [5, 32]
            (method_invocation [5, 4] - [5, 31]
              object: (field_access [5, 4] - [5, 14]
                object: (identifier [5, 4] - [5, 10])
                field: (identifier [5, 11] - [5, 14]))
              name: (identifier [5, 15] - [5, 22])
              arguments: (argument_list [5, 22] - [5, 31]
                (field_access [5, 23] - [5, 30]
                  object: (identifier [5, 23] - [5, 28])
                  field: (identifier [5, 29] - [5, 30]))))))))))

```
So we can see that an AST of a simple Java class includes a lot of information. Actually, `tree-sitter`
 built what is called Concrete Syntax Tree (CST or also known as “parse 
tree”) which includes additional information related to the syntax of 
the language. Notice how `tree-sitter` was able to identify 
and track the exact line and column numbers for each node of the tree 
(they are specified between the square brackets `[]`).


Also, `tree-sitter` is really powerful because it could parse any programming language, as long as there is a grammar that describes the language.


AST are widely used in different applications:


* compilers uses AST as an intermediate representation of the program 
which is then converted to a binary executable (specific for the CPU 
architecture)
* advanced text editors and IDEs uses AST to highlight the source code
 and to perform other complex operations (for example the ability of 
select specific blocks of code using shortkeys)
* source code analysis tools (like SAST, code linter, etc..) use AST 
to quickly parse the source code and look for specific patterns


SAST tools can leverage this formal representation of the source 
code, to perform static analysis and apply complex checks to detect 
suspicious and problematic patterns.


Semgrep uses (also) `tree-sitter` to get the CST and then translates it to the AST (using a [custom parser](https://github.com/returntocorp/ocaml-tree-sitter-semgrep)) which is then used to match patterns defined by rules.


Now let’s see how we can write our first simple rule using the Semgrep engine.


### Matching Spring unauthenticated routes using custom semgrep rule


Semgrep includes a public [registry](https://semgrep.dev/explore)
 of rules which covers a lot of programming languages. So you can 
immediately start using them and scan your project to identify possible 
security issues.


But an interesting feature of semgrep, is that anyone can create 
custom rules. Furthermore, creating custom rules is fairly easy as it 
doesn’t require to know a specific programming language, as they are 
defined by simple `YAML` files.


Now, let’s say we are developing a Java application using Spring MVC 
framework. Let’s assume that the team agreed on using Java Spring 
annotations (and Spring Security) to perform authorization checks for 
each route exposed by the application.


For example let’s say we have the following REST controller which exposes few endpoints:



```
@RestController
public class UserController {
 
    @Autowired
    UserService userService;
 
    @GetMapping("/users")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<List<User>> getAll() {

        return new ResponseEntity<>(userService.getAll(), HttpStatus.OK);
    }
    
    @GetMapping("/users/{id}")
    @PreAuthorize("hasRole('USER')")
    public ResponseEntity<User> getById(@PathVariable long id) {

        Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        
        if (principal instanceof MyUserDetails) {
  			long userId = ((MyUserDetails)principal).getId();
            // If current user `id` is not equal to the `id` parameter return forbidden error
            if(!userId.equals(id)){
                throw new ResponseStatusException(HttpStatus.FORBIDDEN);
            }
		} else {
  			throw new ResponseStatusException(HttpStatus.FORBIDDEN);
		}
        
        Optional<User> user = userService.getById(id);
        if (user.isPresent()) {
            return new ResponseEntity<>(user.get(), HttpStatus.OK);
        } else {
            throw new RecordNotFoundException();
        }
    }
}

```
The previous controller looks safe. We are using the `@PreAuthorize` annotation to achieve the following:


* Only users with `ADMIN` role can get all users information
* Only users with `USER` role can get their own details


Now let’s imagine someone (maybe a new junior developer who just 
joined the team, with lack of experience) is implementing a new features
 that should allow only the administrator to delete a user.


This would require to add another handler to the `UserController` (this time using `@DeleteMapping` annotation) as follows:



```
@DeleteMapping("/users/{id}")
public ResponseEntity<List<User>> deleteUser(@PathVariable long id) {
 
    Optional<User> user = userService.getById(id);
    if (user.isPresent()) {
        userService.deleteUser(id);
        return new ResponseEntity<>("User has been deleted!", HttpStatus.OK);
    } else {
        throw new RecordNotFoundException();
    }
}

```
Unfortunately, the new route `/users/{id}` does not specify any authorization check (the `@PreAuthorize()`
 annotation is missing) so anyone (including unauthenticated users) 
would be able to delete any user. This is of course a trivial error and 
it could be detected manually, but imagine if you have hundreds of 
controllers, each one with hundreds of routes: it will be impractical 
(if not impossible) to detect the issue by looking at them manually.


Instead, using the following semgrep custom rule, we can easily 
detect such issues and prevent the vulnerable code to be deployed in our
 application:



```
rules:
  - id: spring-unauthenticated-route
    patterns:
      - pattern-inside: |
          @RestController
          class $CONTROLLER{ 
            ...
          }          
      - pattern-inside: |
          @$MAPPING($ROUTE)
          $RET $METHOD(...) {...}          
      - metavariable-regex:
          metavariable: $MAPPING
          regex: (GetMapping|PostMapping|DeleteMapping|PutMapping|PatchMapping)    
      - pattern-not: |
          @PreAuthorize(...)
          $METHOD(...){...}          
      - focus-metavariable:
          - $ROUTE
    message: >
      The route $ROUTE is exposed to unauthenticated users. Please verify
      this is expected behaviour, otherwise add the proper authentication/authorization checks.      
    languages:
      - java
    severity: WARNING

```
Let’s go through the rule step by step:


* First we defined an `id`: this is just a unique identifier for the rule.
* Then we have the `patterns` operator: this is the most 
important part of the rule, because it defines which patterns we want to
 match. Every child node of the `patterns` operator must be true in order to get a match (it acts as the logic `AND` operator).
* The `pattern-inside` operator matches findings that reside
 within its expression. Since we are interested in Spring RestController
 classes we can use the `pattern-inside` to only match classes with the `@RestController`
 annotation. Notice that since we want to match any controller class 
(and we don’t know the class name in advance) we are using the `$CONTROLLER` **metavariable**.
 In semgrep, a metavariable is an abstraction to match something that 
you don’t know the value yet (similar to capture groups in regular 
expressions). We can declare a metavariable by prepending the `$` sign to a variable name of our choice (it must be uppercase).
* Another `pattern-inside` is used: in this case we want to match all the methods that have the annotation `@$MAPPING`.
 Basically this is another metavariable used to match all the Spring 
annotation that map some HTTP request to the method. Since the HTTP 
request can have different HTTP methods, we want to match all of them, 
so we can use the `metavariable-regex` operator to define 
our regex. This is simply a regex expression to match one of the 
available mapping annotation provided by Spring (in this case `(GetMapping|PostMapping|DeleteMapping|PutMapping|PatchMapping)`) . Notice that in this pattern we are also using a special operator `...` called **ellipsis**:
 this is used to abstract away a sequence of zero or more items. 
Basically we are saying that we are not interested in the method 
arguments or in the method body.
* Then we use the `pattern-not` operator: since our goal is 
to match routes that are missing the authorization check, we can use 
this operator to find code that does not match this expression (hence it
 is missing the authorization check).
* Finally we use the `focus-metavariable` just to highlight the routes that matched our pattern (the ones that are missing the `@PreAuthorize` annotation).
* The other fields (`message`, `languages` and `severity`)
 are just metadata that is used by semgrep to provide info about the 
findings. Notice that we can refer to metavariables inside the message: 
the metavariable will be resolved automatically by semgrep when there is
 a match.


You can try and play with this rule using the semprep playground [here](https://semgrep.dev/playground/s/DWqq).
 Just click on the “Run” button or press “Ctrl\-Enter” to run the rule 
against the code on the right side of the screen. You should see 1 match
 at line 38, as shown below:


![semgrep](Writing%20your%20first%20custom%20Semgrep%20rule%20-%20Dock12%20-%20Sorint.Lab_files/semgrep.png)


If you want to test your semgrep skills, try to modify the rule to:


* match also when using the generic `@RequestMapping(...)` annotation
* match only routes that are available to users with `ADMIN` role


### Conclusion


This was just a brief introduction to semgrep, a really powerful 
tool. There are a lot of more complex operators and techniques available
 (i.e. taint mode, autofix, etc..) so I’d encourage you to read the 
official [documentation](https://semgrep.dev/docs/).


If you want to learn more about semgrep and create more advanced rules, I’d suggest to start practicing the [semgrep tutorial](https://semgrep.dev/learn).


You can even contribute by publishing your rules to the public [semgrep\-rules](https://github.com/returntocorp/semgrep-rules) GitHub repository and help other developers to write more secure code!




Comment EditorNameLog inPost
















* Theme by [github\-style](https://github.com/MeiK2333/github-style)

















Autofix \| Semgrep










[Skip to main content](#__docusaurus_skipToContent_fallback)[![Semgrep logo](Autofix%20_%20Semgrep_files/semgrep-icon-text-horizontal.svg)](https://semgrep.dev/)[Registry](https://semgrep.dev/explore)[Playground](https://semgrep.dev/editor)[Products](#)* [Semgrep Code](https://semgrep.dev/products/semgrep-code/)
* [Semgrep Supply Chain](https://semgrep.dev/products/semgrep-supply-chain)
* [Semgrep Secrets](https://semgrep.dev/products/semgrep-secrets)
[Pricing](https://semgrep.dev/pricing)[Docs](https://semgrep.dev/docs/)[Knowledge base](https://semgrep.dev/docs/kb)[Login](https://semgrep.dev/orgs/-/)* [Docs home](https://semgrep.dev/docs/)
* Write rules
	+ [Overview](https://semgrep.dev/docs/writing-rules/overview)
	+ [Pattern examples](https://semgrep.dev/docs/writing-rules/pattern-examples)
	+ [Pattern syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
	+ [Custom rule examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
	+ [Rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax)
	+ [Testing rules](https://semgrep.dev/docs/writing-rules/testing-rules)
	+ [Private rules](https://semgrep.dev/docs/writing-rules/private-rules)
	+ [Autofix](https://semgrep.dev/docs/writing-rules/autofix)
	+ [Generic pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)
	+ [Metavariable analysis](https://semgrep.dev/docs/writing-rules/metavariable-analysis)
	+ [Troubleshooting rules](https://semgrep.dev/docs/troubleshooting/rules)
	+ [Experiments 🧪](https://semgrep.dev/docs/writing-rules/experiments/introduction)
	+ [Data\-flow analysis](https://semgrep.dev/docs/writing-rules/data-flow/data-flow-overview)
	+ [SAST and rule\-writing glossary](https://semgrep.dev/docs/writing-rules/glossary)
* 
* Write rules
* Autofix
On this page* [Rule writing](https://semgrep.dev/docs/tags/rule-writing)

Autofix
=======


Autofix is a Semgrep feature where rules contain suggested fixes to resolve findings.


Semgrep's rule format supports a `fix:` key that supports 
the replacement of metavariables and regex matches with potential fixes.
 This allows for value capture and rewriting. With rules that make use 
of the autofix capability, you can resolve findings as part of your code
 review workflow. Semgrep suggests these fixes through GitHub PR or 
GitLab MR comments.


You can apply the autofix directly to the file using the `--autofix` flag. To test the autofix before applying it, use both the `--autofix` and `--dryrun` flags.


Example autofix snippet[​](#example-autofix-snippet "Direct link to Example autofix snippet")
---------------------------------------------------------------------------------------------


Sample autofix (view in [Playground](https://semgrep.dev/s/R6g)):



```
rules:  
- id: use-sys-exit  
  languages:  
  - python  
  message: |  
    Use `sys.exit` over the python shell `exit` built-in. `exit` is a helper  
    for the interactive shell and is not be available on all Python implementations.  
    https://stackoverflow.com/a/6501134  
  pattern: exit($X)  
  fix: sys.exit($X)  
  severity: WARNING  

```

Create autofix rules[​](#create-autofix-rules "Direct link to Create autofix rules")
------------------------------------------------------------------------------------


See how to create an autofix rule in **Transforming code with Semgrep autofixes** video:



Autofix with regular expression replacement[​](#autofix-with-regular-expression-replacement "Direct link to Autofix with regular expression replacement")
---------------------------------------------------------------------------------------------------------------------------------------------------------


A variant on the `fix` key is `fix-regex`, which applies regular expression replacements (think `sed`) to matches found by Semgrep.


`fix-regex` has two required fields:


* `regex` specifies the regular expression to replace within the match found by Semgrep
* `replacement` specifies what to replace the regular expression with.


`fix-regex` also takes an optional `count` field, which specifies how many occurrences of `regex` to replace with `replacement`, from left\-to\-right and top\-to\-bottom. By default, `fix-regex` will replace all occurrences of `regex`. If `regex` does not match anything, no replacements are made.


The replacement behavior is identical to the `re.sub` function in Python. See these [Python docs](https://docs.python.org/3/library/re.html#re.sub) for more information.


An example rule with `fix-regex` is shown below. `regex` uses a capture group to greedily capture everything up to the final parenthesis in the match found by Semgrep. `replacement` replaces this with everything in the capture group (`\1`), a comma, `timeout=30`, and a closing parenthesis. Effectively, this adds `timeout=30` to the end of every match.



```
rules:  
- id: python.requests.best-practice.use-timeout.use-timeout  
  patterns:  
  - pattern-not: requests.$W(..., timeout=$N, ...)  
  - pattern-not: requests.$W(..., **$KWARGS)  
  - pattern-either:  
    - pattern: requests.request(...)  
    - pattern: requests.get(...)  
    - pattern: requests.post(...)  
    - pattern: requests.put(...)  
    - pattern: requests.delete(...)  
    - pattern: requests.head(...)  
    - pattern: requests.patch(...)  
  fix-regex:  
    regex: '(.*)\)'  
    replacement: '\1, timeout=30)'  
  message: |  
    'requests' calls default to waiting until the connection is closed.  
    This means a 'requests' call without a timeout will hang the program  
    if a response is never received. Consider setting a timeout for all  
    'requests'.  
  languages: [python]  
  severity: WARNING  

```

Remove a code detected by a rule[​](#remove-a-code-detected-by-a-rule "Direct link to Remove a code detected by a rule")
------------------------------------------------------------------------------------------------------------------------


Improve your code quality by cleaning up stale code automatically. Remove code that an autofix rule detected by adding the `fix` key with `""`, an empty string.


For example:



```
 - id: python-typing  
   pattern: from typing import $X  
   fix: ""  
   languages: [ python ]  
   message: found one  
   severity: ERROR  

```

When an autofix is applied, this rule removes the detected code.



---

Not finding what you need in this doc? Ask questions in our [Community Slack group](https://go.semgrep.dev/slack), or see [Support](https://semgrep.dev/docs/support/) for other ways to get help.

**Tags:*** [Rule writing](https://semgrep.dev/docs/tags/rule-writing)
[Edit this page](https://github.com/semgrep/semgrep-docs/edit/main/docs/writing-rules/autofix.md)Last updated on **Jun 12, 2024**[PreviousPrivate rules](https://semgrep.dev/docs/writing-rules/private-rules)[NextGeneric pattern matching](https://semgrep.dev/docs/writing-rules/generic-pattern-matching)* [Example autofix snippet](#example-autofix-snippet)
* [Create autofix rules](#create-autofix-rules)
* [Autofix with regular expression replacement](#autofix-with-regular-expression-replacement)
* [Remove a code detected by a rule](#remove-a-code-detected-by-a-rule)
Community* [Slack](https://go.semgrep.dev/slack)
* [GitHub](https://github.com/semgrep/semgrep)
* [Twitter](https://twitter.com/semgrep)
Learn* [Docs](https://semgrep.dev/docs/)
* [Examples](https://semgrep.dev/docs/writing-rules/rule-ideas)
* [Tour](https://semgrep.dev/learn)
Product* [Privacy](https://semgrep.dev/privacy)
* [Issues](https://github.com/semgrep/semgrep/issues)
* [Terms of service](https://semgrep.dev/terms)
About* [Semgrep blog](https://semgrep.dev/blog/)
* [About us](https://semgrep.dev/about)
* [Semgrep release updates](https://twitter.com/semgrepreleases)
Copyright © 2024 Semgrep, Inc. Semgrep®️ is a registered trademark of Semgrep, Inc. These docs are made with Docusaurus.


![](https://www.facebook.com/tr?id=1153975365383030&ev=PageView&noscript=1)



![](Autofix%20_%20Semgrep_files/adsct.gif)![](Autofix%20_%20Semgrep_files/adsct_002.gif)



