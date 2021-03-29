import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout
        try:
            self._socket = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientError(err)

    def put(self, metric, value, timestamp=None):
        timestamp = str(timestamp or int(time.time()))
        send_data = f'put {metric} {value} {timestamp}\n'.encode('utf8')

        try:
            self._socket.sendall(send_data)
            responce = self._socket.recv(1024)
            if b'ok\n' not in responce:
                raise ClientError
        except socket.error as err:
            raise ClientError(err)

    def get(self, metric):
        metric_dict = {}
        send_data = f'get {metric}\n'.encode('utf8')

        try:
            self._socket.sendall(send_data)
            responce = str(self._socket.recv(1024))
        except Exception:
            raise ClientError

        try:
            self._socket.sendall(send_data)
            response = self._socket.recv(1024)
            if b'ok' not in response:
                raise ClientError

            response = str(response).strip('\n').split('\\n')

            for m in response:
                metrics = m.split(' ')
                if len(metrics) == 3:
                    metric_key = metrics[0]
                    metric_value = float(metrics[1])
                    metric_timestamp = int(metrics[2])
                    metric_list = metric_dict.get(metric_key, [])
                    metric_list.append((metric_timestamp, metric_value))
                    metric_dict.update({metric_key: sorted(metric_list)})
                elif metrics not in [["b'ok"], [""], ["'"]]:
                    raise ClientError

            return metric_dict

        except Exception as err:
            raise ClientError(err)
