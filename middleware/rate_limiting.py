import time
from flask import request
from collections import deque

error_messages = {
    'rate_limit_exceeded': 'Rate limit exceeded. Please try again in {seconds} seconds.'
}

call_history = {}


def rate_limited(max_calls=5, time_frame=60):
    def decorator(handler):
        def wrapper(*args, **kwargs):
            ip_address = request.remote_addr

            if ip_address not in call_history:
                call_history[ip_address] = deque()
            
            queue = call_history[ip_address]
            current_time = time.time()
            
            while len(queue) > 0 and current_time - queue[0] > time_frame:
                queue.popleft()
            
            if len(queue) > max_calls:
                time_passed = current_time - queue[0]
                time_to_wait = int(time_frame - time_passed)
                error_message = error_messages['rate_limit_exceeded'].format(seconds=time_to_wait)
                return error_message, 429

            queue.append(current_time)

            return handler(*args, **kwargs)

        return wrapper

    return decorator