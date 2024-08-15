import re

def process_log_file(input_file: str, output_file: str):
    # Durum kodları açıklamaları
    status_code_meanings = {
        '200': 'OK',
        '301': 'Moved Permanently',
        '302': 'Found',
        '400': 'Bad Request',
        '401': 'Unauthorized',
        '403': 'Forbidden',
        '404': 'Not Found',
        '500': 'Internal Server Error',
        '502': 'Bad Gateway',
        '503': 'Service Unavailable',
        '504': 'Gateway Timeout'
    }

    # Log dosyasını oku
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Başlıkları belirleyin
    headers = ["IP Address", "Request Method", "URL", "Status Code", "Status Meaning", "Byte Size", "User Agent", "Timestamp"]
    
    # Formatlı logları saklamak için bir liste oluşturun
    formatted_lines = []

    # Logları işleyin
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Logu parçalayın
        match = re.match(r'^(.*?) - - \[(.*?)\] "(.*?)" (\d{3}) (\d+) "(.*?)" "(.*?)"$', line)
        if match:
            ip_address = match.group(1)
            timestamp = match.group(2)
            request = match.group(3)
            status_code = match.group(4)
            byte_size = match.group(5)
            user_agent = match.group(7)

            # Durum kodu anlamını al
            status_meaning = status_code_meanings.get(status_code, 'Unknown Status Code')

            # İstek metodunu ve URL'yi ayırın
            request_parts = request.split(' ', 1)
            if len(request_parts) == 2:
                request_method, url = request_parts
            else:
                request_method = request_parts[0]
                url = ""

            # Formatlı log satırını oluşturun
            formatted_line = (
                f"{headers[0]}: {ip_address}\t"
                f"{headers[1]}: {request_method}\t"
                f"{headers[2]}: {url}\t"
                f"{headers[3]}: {status_code}\t"
                f"{headers[4]}: {status_meaning}\t"
                f"{headers[5]}: {byte_size}\t"
                f"{headers[6]}: {user_agent}\t"
                f"{headers[7]}: {timestamp}"
            )
            formatted_lines.append(formatted_line)
    
    # Formatlı logları dosyaya yazın
    with open(output_file, 'w') as f:
        f.write('\n'.join(formatted_lines))

# Kullanım
input_log_file = 'log_file.log'  # Giriş log dosyası
output_formatted_file = 'formatted_logs.txt'  # Çıkış dosyası
process_log_file(input_log_file, output_formatted_file)
