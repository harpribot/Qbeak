from src.utils.handlers import Handler

handle = Handler()
brainwit_handle = handle.wit().brain()


def trait_if_present(processed_query):
    triggers_dict = processed_query[1]
    if triggers_dict is None:
        return None
    trait = triggers_dict['intent'][0] if 'intent' in triggers_dict else None
    return trait


def get_trait_and_confidence(brainwit_processed_query):
    triggers_dict = brainwit_processed_query[1]
    if triggers_dict is None:
        return None, 0
    trait = triggers_dict['intent'][0] if 'intent' in triggers_dict else None
    confidence = triggers_dict['intent'][1] if 'intent' in triggers_dict else 0
    return trait, confidence

