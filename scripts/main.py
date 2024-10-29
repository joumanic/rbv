from event_handler import EventHandler

if __name__ == "__main__":
    handler = EventHandler()
    event = {"trigger": True} # Simulate an event
    response = handler.handle_event(event)
    print(response)