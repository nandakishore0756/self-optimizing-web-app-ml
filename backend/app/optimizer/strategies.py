OPTIMIZATION_STRATEGIES = [
    {"key": "caching", "name": "Enable response caching",
     "description": "Reduce repeated expensive computations and database reads."},
    {"key": "database", "name": "Optimize database queries",
     "description": "Enable application-level query optimization and smaller pagination."},
    {"key": "pagination", "name": "Reduce pagination limit",
     "description": "Lower the amount of data returned by heavy list endpoints."},
    {"key": "heavy_components", "name": "Disable heavy non-essential components",
     "description": "Turn off expensive optional UI work during high-load periods."},
]
