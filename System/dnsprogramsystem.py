from flask import Flask, request, render_template
import dns.resolver
import requests

app = Flask(__name__)

def generate_confusable_domains(domain):
    substitutions = {'o': ['0'], 'i': ['1', 'l'], 'l': ['1', 'i'], 's': ['5'], 'a': ['@']}
    variations = [domain]
    for i, char in enumerate(domain):
        if char in substitutions:
            for sub in substitutions[char]:
                variations.append(domain[:i] + sub + domain[i+1:])
    for i in range(len(domain)):
        variations.append(domain[:i+1] + domain[i] + domain[i+1:])
    for i in range(len(domain)):
        variations.append(domain[:i] + domain[i+1:])
    return list(set(variations))

def check_domain_registration(domains):
    registered_domains = []
    for domain in domains:
        if domain.endswith('.') or '..' in domain or not domain:
            continue
        try:
            dns.resolver.resolve(domain)
            registered_domains.append(domain)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            continue
        except dns.resolver.NoNameservers:
            continue
    return registered_domains

def check_domain_with_virustotal(domain):
    url = "https://www.virustotal.com/api/v3/domains/{}".format(domain)
    headers = {"x-apikey": "1ac4397532b0ac570437f0c94479f0a7dca6854f50091ebab046b4c8a83af35b"}  # Replace with your actual VirusTotal API key
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        malicious_votes = data['data']['attributes']['last_analysis_stats']['malicious']
        if malicious_votes > 0:
            return True, data['data']['attributes']['last_analysis_results']
        else:
            return False, None
    else:
        return False, None

def analyze_domain_legitimacy(domains):
    analysis_results = {}
    for domain in domains:
        is_malicious, analysis_details = check_domain_with_virustotal(domain)
        analysis_results[domain] = {'is_malicious': is_malicious, 'details': analysis_details}
    return analysis_results

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/check', methods=['POST'])
def check():
    domain = request.form['domain']
    confusable_domains = generate_confusable_domains(domain)
    registered_domains = check_domain_registration(confusable_domains)
    analysis_results = analyze_domain_legitimacy(registered_domains)
    return render_template('results.html', analysis_results=analysis_results, domain=domain)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)
