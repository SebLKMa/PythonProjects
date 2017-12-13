from stix.core import STIXPackage
from stix.incident import Incident
from stix.common import InformationSource
from cybox.common import Time
from datetime import datetime
from stix.common import Identity
from stix.incident import Time as incidentTime  # different type than common:Time
from stix.incident import Incident, ImpactAssessment
from stix.incident.impact_assessment import Effects
from stix.common import References

# setup stix document
stix_package = STIXPackage()

# add incident and confidence
breach = Incident()
breach.description = "Parity Wallet Hacked"
breach.confidence = "High" # investigators were able to thoroughly validate the incident, Low means not yet validated

# stamp with reporter
breach.reporter = InformationSource()
breach.reporter.description = "https://paritytech.io/blog/security-alert.html"

breach.reporter.time = Time()
breach.reporter.time.produced_time = datetime.strptime("2017-11-08","%Y-%m-%d") # when they submitted it

breach.reporter.identity = Identity()
breach.reporter.identity.name = "parity technologies ltd"

# set incident-specific timestamps
breach.time = incidentTime()
breach.title = "The Multi-sig Hack"
breach.time.initial_compromise = datetime.strptime("2017-11-06", "%Y-%m-%d")
breach.time.incident_discovery = datetime.strptime("2017-11-08", "%Y-%m-%d")
#breach.time.restoration_achieved = datetime.strptime("2012-08-10", "%Y-%m-%d")
breach.time.incident_reported = datetime.strptime("2017-11-08", "%Y-%m-%d")

# add the impact
impact = ImpactAssessment()
impact.effects = Effects("Estimated Loss of $280m in Ether")
breach.impact_assessment = impact

# add the victim
victim = Identity()
victim.name = "Cappasity"
breach.add_victim(victim)
victim2 = Identity()
victim2.name = "Who else ?"
breach.add_victim(victim2)

# add Information Sources
infoSource = InformationSource();
infoSource.add_description("https://news.ycombinator.com/item?id=15642856")
infoSource.add_description("https://www.theregister.co.uk/2017/11/10/parity_280m_ethereum_wallet_lockdown_hack/")
breach.Information_Source = infoSource;

stix_package.add_incident(breach)
print(stix_package.to_json())
