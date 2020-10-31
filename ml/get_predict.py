from typing import Dict, List


def get_predicts(user_id: int) -> Dict[str, List[int]]:
    '''
    :param user_id : id from "data.User"
    :return: {'books': [book_1_id, book_2_id, ...],
              'events': [event_1_id, event_2_id, ...],
              'services': [service_1_id, service_2_id, service_3_id, ...]
             }
    '''
    books = []
    events = []
    services = []
    return {
        'books': books,
        'events': events,
        'services': services,
    }
