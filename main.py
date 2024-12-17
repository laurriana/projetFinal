import service
import time
import threading

def main():
    stop_event = False
    print("i can't wait for finals to be over...")
    time.sleep(1)
    print("please enter your codes.")
    
    read_function = threading.Thread(target=service.read_button, args=(stop_event,), daemon=True)
    read_function.start()

    user_codes = service.creation_code()
    stop_event = True
    print(f"your code is: {user_codes}")

    time.sleep(2)

    print("it is now time to unlock your lock!")
    attempt_codes = service.enter_code()
    print(f"you wrote: {attempt_codes}")
    
    service.compare_codes(user_codes, attempt_codes)

if __name__ == "__main__":
    main()