# context_processors.py
def navigation(request):
    """Context processor that provides navigation items to all templates."""
    nav_items = [
        {
            'name': 'Home',
            'url': 'home:home',
            'is_active': request.path == '/',
            'dropdown': [
                {'name': 'About Us', 'url': 'about:about', 'icon': 'M8 12l4-4 4 4m0 4l-4 4-4-4'},
                {'name': 'Our Mission', 'url': 'about:about', 'icon': 'M12 4v4h4m4 0h-4V4h-4v4h4m4 12v-4h-4v4h-4v4h4v-4h4v4'},
                {'name': 'Our Vision', 'url': 'about:about', 'icon': 'M13 10V3L4 14h7v7l9-11h-7z'}
            ]
        },
        {
            'name': 'About',
            'url': 'about:about',
            'is_active': request.path.startswith('/about'),
            'dropdown': [
                {'name': 'Our Leadership', 'url': 'about:about', 'icon': 'M12 4v1m-1 4h1m0 6h2m-1 3h2'},
                {'name': 'Our History', 'url': 'about:about', 'icon': 'M8 7h.01M12 7h.01M16 7h.01M12 11h8m-8 4h8m-8 4h8m-10-8H3m2-6H3'},
                {'name': 'Ministries', 'url': 'about:about', 'icon': 'M5 8h.01M19 8h.01M12 12h.01M12 16h.01M12 20h8m-8-4h8M4 12h8m-8 4h8'}
            ]
        },
        {
            'name': 'Watch | Listen | Read',
            'url': 'watch:watch',
            'is_active': request.path.startswith('/watch'),
            'dropdown': [
                {'name': 'Sermons', 'url': 'watch:watch', 'icon': 'M12 4v8m0 0v8m0-8h4m-4 0H8'},
                {'name': 'Podcasts', 'url': 'listen:listen', 'icon': 'M12 4v2m0 10v2m-7-7h2m10 0h2m-4-4h2m-6 0h2'},
                {'name': 'Articles', 'url': 'read:read', 'icon': 'M12 4v4m0 4v4m-8-8h4m4 0h4m-4-4v4m-8-4h4'}
            ]
        },
        {
            'name': 'Listen',
            'url': 'listen:listen',
            'is_active': request.path.startswith('/listen'),
            'dropdown': [
                {'name': 'Podcasts', 'url': 'listen:listen', 'icon': 'M12 4v4m0 4v4m-8-8h4m4 0h4m-4 4v4m-8-4h4m-4-4h4'},
                {'name': 'Music', 'url': 'listen:listen', 'icon': 'M9 19V6h6v13m-9-6h2V5a2 2 0 112 0v7h2a2 2 0 112 0h2'},
                {'name': 'Audiobooks', 'url': 'listen:listen', 'icon': 'M12 4v16m0 0v-4h8v4m-8-8V4H4v8h8z'}
            ]
        },
        {
            'name': 'Read',
            'url': 'read:read',
            'is_active': request.path.startswith('/read'),
            'dropdown': [
                {'name': 'Articles', 'url': 'read:read', 'icon': 'M12 4v16m-6-8h12'},
                {'name': 'Books', 'url': 'read:read', 'icon': 'M12 4v16m-6-8h12'},
                {'name': 'Devotionals', 'url': 'read:read', 'icon': 'M5 5h14v14H5z'}
            ]
        },
        {
            'name': 'Ministries',
            'url': 'ministries:ministries',
            'is_active': request.path.startswith('/ministries'),
            'dropdown': [
                {'name': 'Worship', 'url': 'ministries:ministries', 'icon': 'M9 19V6h6v13m-9-6h2V5a2 2 0 112 0v7h2a2 2 0 112 0h2'},
                {'name': 'Discipleship', 'url': 'ministries:ministries', 'icon': 'M12 4v16m0 0v-4h8v4m-8-8V4H4v8h8z'},
                {'name': 'Community Outreach', 'url': 'ministries:ministries', 'icon': 'M12 4v16m0 0v-4h8v4m-8-8V4H4v8h8z'}
            ]
        },
        {
            'name': 'Events',
            'url': 'events:events',
            'is_active': request.path.startswith('/events'),
            'dropdown': [
                {'name': 'Upcoming Events', 'url': 'events:events', 'icon': 'M12 4v16m-6-8h12'},
                {'name': 'Past Events', 'url': 'events:events', 'icon': 'M12 4v16m-6-8h12'},
                {'name': 'Conferences', 'url': 'events:events', 'icon': 'M12 4v8m-4-4h8m0 0H4'}
            ]
        },
        {
            'name': 'Contact',
            'url': 'contact:contact',
            'is_active': request.path.startswith('/contact'),
            'dropdown': [
                {'name': 'Contact Form', 'url': 'contact:contact', 'icon': 'M12 4v16m-6-8h12'},
                {'name': 'Locations', 'url': 'contact:contact', 'icon': 'M12 4v16m-6-8h12'},
                {'name': 'Prayer Requests', 'url': 'contact:contact', 'icon': 'M12 4v16m-6-8h12'}
            ]
        }
    ]
    
    return {'nav_items': nav_items}