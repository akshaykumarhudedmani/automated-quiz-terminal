import time
import sys

try:
    import msvcrt
    WINDOWS = True
except ImportError:
    WINDOWS = False
    import select

def get_choice_with_timeout(timeout_seconds: int) -> str:
    """
    Waits for a single key press (A, B, C, or D) with a real-time countdown.
    
    Args:
        timeout_seconds (int): Maximum time in seconds allowed for answering.
        
    Returns:
        str: Selected option ('A', 'B', 'C', 'D') in uppercase, or None if timed out.
    """
    if timeout_seconds is None or timeout_seconds <= 0:
        # No timer, wait indefinitely for a single key press
        sys.stdout.write("Your choice (A/B/C/D): ")
        sys.stdout.flush()
        while True:
            char = _read_key()
            if char in ['A', 'B', 'C', 'D']:
                sys.stdout.write(f"{char}\n")
                sys.stdout.flush()
                return char
            elif char == '\x03': # Ctrl+C
                raise KeyboardInterrupt
            time.sleep(0.05)

    start_time = time.time()
    last_sec = timeout_seconds
    
    sys.stdout.write(f"\r[Time left: {last_sec}s] Enter your choice (A/B/C/D): ")
    sys.stdout.flush()

    while True:
        elapsed = time.time() - start_time
        remaining = int(timeout_seconds - elapsed)
        
        if remaining <= 0:
            sys.stdout.write(f"\r[Time left: 0s] Time's up!                           \n")
            sys.stdout.flush()
            return None
            
        if remaining != last_sec:
            sys.stdout.write(f"\r[Time left: {remaining}s] Enter your choice (A/B/C/D): ")
            sys.stdout.flush()
            last_sec = remaining
            
        char = _read_key_non_blocking()
        if char:
            if char in ['A', 'B', 'C', 'D']:
                sys.stdout.write(f"\r[Time left: {remaining}s] Selected: {char}                        \n")
                sys.stdout.flush()
                return char
            elif char == '\x03': # Ctrl+C
                raise KeyboardInterrupt
                
        time.sleep(0.05)

def _read_key():
    """Helper to read a single key blockingly."""
    if WINDOWS:
        try:
            char = msvcrt.getch()
            return char.decode('utf-8', errors='ignore').upper()
        except Exception:
            return None
    else:
        try:
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch.upper()
        except Exception:
            # Fallback to standard input if tty is not available
            inp = sys.stdin.readline().strip().upper()
            return inp[0] if inp else None

def _read_key_non_blocking():
    """Helper to read a single key nonblockingly. Returns None if no key pressed."""
    if WINDOWS:
        if msvcrt.kbhit():
            try:
                char = msvcrt.getch()
                return char.decode('utf-8', errors='ignore').upper()
            except Exception:
                return None
        return None
    else:
        try:
            # Unix non-blocking read using select
            rlist, _, _ = select.select([sys.stdin], [], [], 0.0)
            if rlist:
                import tty
                import termios
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch.upper()
        except Exception:
            pass
        return None
