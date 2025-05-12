import logging

from datetime import datetime


class BaseLogger(logging.Logger):
     def __init__(self, path: str) -> None:
          super().__init__(name="LOG")
          self.setLevel(logging.INFO)
          
          logger_handler = logging.FileHandler(
               filename=path + datetime.now().strftime("%Y-%m-%d") + ".txt",
          )
          format = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
          
          logger_handler.setFormatter(format)
          self.addHandler(logger_handler)
     
     
     
class Logger:
     
     @property
     def api(self) -> BaseLogger:
          return BaseLogger(
               path="app/logs/api"
          )
          
     
     @property
     def db(self) -> BaseLogger:
          return BaseLogger(
               path="app/logs/db"
          )
          
     
     @property
     def errors(self) -> BaseLogger:
          return BaseLogger(
               path="app/logs/errors/"
          )
          
          
     @property
     def redis(self) -> BaseLogger:
          return BaseLogger(
               path="app/logs/redis/"
          )
          
          
     @property
     def http(self) -> BaseLogger:
          return BaseLogger(
               path="app/logs/http"
          )
          
          
logging_ = Logger()