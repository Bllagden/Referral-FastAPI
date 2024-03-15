
```
fastapi_auth_1
├─ .gitignore
├─ .vscode
│  ├─ launch.json
│  └─ settings.json
├─ alembic.ini
├─ main.py
├─ pdm.lock
├─ pyproject.toml
├─ README.md
├─ src
│  ├─ alembic
│  │  ├─ env.py
│  │  ├─ README
│  │  ├─ script.py.mako
│  │  └─ versions
│  │     ├─ 2024_03_14_173152-19792d7102ce_initial_migration.py
│  │     └─ 2024_03_15_020808-dff0300e2336_referrals.py
│  ├─ api
│  │  ├─ ref_codes
│  │  │  ├─ codes.py
│  │  │  ├─ router.py
│  │  │  └─ schemas.py
│  │  ├─ users
│  │  │  ├─ auth.py
│  │  │  ├─ dependencies.py
│  │  │  ├─ router.py
│  │  │  └─ schemas.py
│  │  └─ __init__.py
│  ├─ app.py
│  ├─ dao
│  │  ├─ base_dao.py
│  │  ├─ codes_dao.py
│  │  ├─ referrals_dao.py
│  │  ├─ users_dao.py
│  │  └─ __init__.py
│  ├─ db
│  │  ├─ base.py
│  │  ├─ dependencies.py
│  │  ├─ engine.py
│  │  ├─ models
│  │  │  ├─ referrals.py
│  │  │  ├─ ref_codes.py
│  │  │  ├─ users.py
│  │  │  └─ __init__.py
│  │  └─ __init__.py
│  ├─ exceptions.py
│  └─ settings.py


└─ tests
   ├─ conftest.py
   ├─ integration_tests
   │  ├─ test_bookings
   │  │  ├─ test_api.py
   │  │  ├─ test_dao.py
   │  │  └─ __init__.py
   │  ├─ test_users
   │  │  ├─ test_api.py
   │  │  └─ __init__.py
   │  └─ __init__.py
   ├─ mock_bookings.json
   ├─ mock_hotels.json
   ├─ mock_rooms.json
   ├─ mock_users.json
   ├─ unit_tests
   │  ├─ test_users
   │  │  ├─ test_dao.py
   │  │  └─ __init__.py
   │  └─ __init__.py
   └─ __init__.py

```