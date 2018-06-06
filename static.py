API_DESC = [
        {
                'api_url': '/v1/',
                'command': 'get',
                'comments': 'Описание доступных методов (этот документ)'
        },
        {
                'api_url': '/v1/users',
                'command': 'get',
                'comments': 'Получить список пользователей'
        },
        {
                'api_url': '/v1/users/{user_id}',
                'command': 'get',
                'comments': 'Получить пользователя user_id'
        },
        {
                'api_url': '/v1/persons',
                'command': 'get',
                'comments': 'Получить список персон'
        },
        {
                'api_url': '/v1/persons/{persons_id}',
                'command': 'get',
                'comments': 'Получить ключевые слова для person_id'
        },
        {
                'api_url': '/v1/persons/rank',
                'command': 'get',
                'comments': 'Получить список персон с их рангами по всем сайтам'
        },
        {
                'api_url': '/v1/persons/rank/{person_id}',
                'command': 'get',
                'comments': 'Получить список рангов по всем сайтам для person_id'
        },
        {
                'api_url': '/v1/sites',
                'command': 'get',
                'comments': 'Получить список сайтов'
        },
        {
                'api_url': '/v1/sites/{site_id}',
                'command': 'get',
                'comments': 'Получить сайт по site_id'
        },
        {
                'api_url': '/v1/persons/rank/date?_from=YYYYMMDDDHHMMSS&_till=YYYYMMDDDHHMMSS',
                'command': 'get',
                'comments': 'Получить список персон с их рангами по всем сайтам за период _from _till'
        },
        {
                'api_url': '/v1/persons/rank/{person_id}/date?_from=YYYYMMDDDHHMMSS&_till=YYYYMMDDDHHMMSS',
                'command': 'get',
                'comments': 'Получить ранг {person_id} по всем сайтам за период _from _till'
        },
]