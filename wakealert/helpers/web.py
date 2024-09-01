from requests import Session

from ..constants import LOGIN_EMAIL, LOGIN_PASSWORD, RUN_WITH_LOGS

HOME_PAGE = "https://lakeridersclub.ch/index.php"
AUTHENTICATION_PAGE = "https://lakeridersclub.ch/membres/connexion.php"
CALENDAR_PAGE = "https://lakeridersclub.ch/membres/reservations.php"


def create_browser_session():
    session = Session()
    session.get(HOME_PAGE)
    return session


def get_session_authorized(session):
    if RUN_WITH_LOGS:
        print("Authenticating")

    session.post(
        url=AUTHENTICATION_PAGE,
        data={
            "adresse_electronique": LOGIN_EMAIL,
            "mot_de_passe": LOGIN_PASSWORD,
            "rester_connecte": 1,
            "action": "se_connecter",
        },
    )


def get_reservations_html(session):
    response = session.get(CALENDAR_PAGE)
    if response.url == HOME_PAGE:
        # The session is not authenticated. Re-authenticate
        get_session_authorized(session)
        authenticated_response = session.get(CALENDAR_PAGE)
        return authenticated_response.text
    else:
        return response.text
