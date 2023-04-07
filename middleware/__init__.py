from aiogram import Dispatcher
from middleware.throttling_middleware import ThrottlingMiddleware
from middleware.maintenance_middleware import MaintenanceMiddleware

def setup_middleware(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(MaintenanceMiddleware())