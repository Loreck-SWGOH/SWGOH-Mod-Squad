from app import create_app
from app.models.event import Event

app = create_app()


@app.context_processor
def context_processor():
    """
    Add events to all templates
    """
    event_list = Event.get_all()
    return dict(events=event_list)
