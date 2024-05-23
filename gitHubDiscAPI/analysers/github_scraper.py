import json

post_data = {}
with open('../data/github_scraper.json', 'r') as file:
    post_data = json.load(file)

# Obsolescence
obsolescence_terms = ["Outdate", "Legacy", "deprecat", "Phasing out", "Obsolete", "Unmaintain"]
obsolescence_terms_lower = [term.lower() for term in obsolescence_terms]

# Dependency issues
dependency_issues_terms = ["Dependency", "conflict", "mismatch", "Package", "Version", "Dependency problem", "Incompatible dependenc"]
dependency_issues_terms_lower = [term.lower() for term in dependency_issues_terms]

# Breaking changes
breaking_changes_terms = ["version", "incompatible", "API changes", "Breaking updates", "Breaking modifications", "Breaking alterations", "Disruptive changes"]
breaking_changes_terms_lower = [term.lower() for term in breaking_changes_terms]

# Security vulnerabilities
security_vulnerabilities_terms = ["security", "Security flaws", "Security risk", "Vulnerabilities", "Exploit", "loopholes", "Attack"]
security_vulnerabilities_terms_lower = [term.lower() for term in security_vulnerabilities_terms]

found_obsolescence = []
found_dependency_issues = []
found_breaking_changes = []
found_security_vulnerabilities = []

for item in post_data:
    for term in obsolescence_terms:
        if term.lower() in item['body'].lower():
            #dict = {'link' : item['link', ]}
            found_obsolescence.append(term)

    for term in dependency_issues_terms:
        if term.lower() in item['body'].lower():
            found_dependency_issues.append(term)

    for term in breaking_changes_terms:
        if term.lower() in item['body'].lower():
            found_breaking_changes.append(term)
        
    for term in security_vulnerabilities_terms:
        if term.lower() in item['body'].lower():
            found_security_vulnerabilities.append(term)

print(len(post_data))

print('found_obsolescence: ', len(found_obsolescence))
print('found_dependency_issues: ',        len(found_dependency_issues))
print('found_breaking_changes: ',         len(found_breaking_changes))
print('found_security_vulnerabilities: ',         len(found_security_vulnerabilities))

print('total: ', len(found_obsolescence) + len(found_dependency_issues) + len(found_breaking_changes) + len(found_security_vulnerabilities))


