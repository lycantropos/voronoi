from datetime import timedelta

from hypothesis import (HealthCheck,
                        settings)

settings.register_profile('default',
                          deadline=timedelta(minutes=10),
                          suppress_health_check=[HealthCheck.filter_too_much,
                                                 HealthCheck.too_slow])
