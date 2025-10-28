'''
2024-01-22 08:30:01 INFO User logged in successfully.
2024-01-22 08:45:23 DEBUG Attempting to connect to the database.
2024-01-22 09:00:45 ERROR Database connection failed.
2024-01-22 09:15:10 INFO Data export completed.
2024-01-22 10:30:55 WARNING Disk usage above 80%.
2024-01-22 11:05:00 DEBUG Starting data backup process.
2024-01-22 11:30:15 ERROR Backup process failed.
2024-01-22 12:00:00 INFO User logged out.
2024-01-22 12:45:05 DEBUG Checking system health.
2024-01-22 13:30:30 INFO Scheduled maintenance.
'''

import sys

def parse_log_line(line: str) -> dict:
    
    parts = line.strip().split(' ', 3)
    if len(parts) < 4:
        return None  
    date, time, level, message = parts
    return {
        'date': date,
        'time': time,
        'level': level.upper(),
        'message': message
    }

def load_logs(file_path: str) -> list:
    
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parsed = parse_log_line(line)
                if parsed:
                    logs.append(parsed)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
   
    level = level.upper()
    return list(filter(lambda log: log['level'] == level, logs))

def count_logs_by_level(logs: list) -> dict:
    
    levels = ['INFO', 'DEBUG', 'ERROR', 'WARNING']
    counts = {lvl: 0 for lvl in levels}
    for log in logs:
        if log['level'] in counts:
            counts[log['level']] += 1
    return counts

def display_log_counts(counts: dict):
    
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<16}| {count}")

def display_logs_details(logs: list, level: str):
    
    print(f"\nДеталі логів для рівня '{level.upper()}':")
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")

def main():
    if len(sys.argv) < 2:
        print("Використання: python main.py <file.txt> [DEBUG]")
        sys.exit(1)

    file_path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level:
        filtered = filter_logs_by_level(logs, level)
        display_logs_details(filtered, level)

if __name__ == "__main__":
    main()