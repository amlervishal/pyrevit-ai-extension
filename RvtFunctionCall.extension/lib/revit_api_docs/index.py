"""
Revit API - Complete Reference Index
Master index for all Revit API documentation and examples
"""

# LIBRARY STRUCTURE
LIBRARY_STRUCTURE = {
    'core/': {
        'document.py': 'Document access, properties, file operations'
    },
    
    'selection/': {
        'selection.py': 'Element selection, filtering, FilteredElementCollector'
    },
    
    'elements/': {
        'creation.py': 'Creating walls, floors, families, geometry, modifications'
    },
    
    'transactions/': {
        'basic_transactions.py': 'Basic transaction patterns',
        'advanced_transactions.py': 'Transaction groups & sub-transactions'
    },
    
    'analysis/': {
        'spatial_analysis.py': 'Room/area analysis, quantities, boundary analysis'
    },
    
    'documentation/': {
        'schedules_sheets.py': 'Creating schedules, sheets, viewports, material takeoffs'
    },
    
    'examples/': {
        'complete_workflows.py': 'End-to-end workflow examples'
    },
    
    'builtin_elements.py': 'Built-in parameters, categories, common elements',
    'quick_reference.py': 'Quick lookup for common operations'
}

# FUNCTIONAL CATEGORIES
FUNCTIONAL_CATEGORIES = {
    '🏗️ ELEMENT CREATION': {
        'files': ['elements/creation.py'],
        'capabilities': [
            'Create walls, floors, ceilings, roofs',
            'Place family instances (doors, windows, furniture)',
            'Create datum elements (levels, grids)',
            'Generate geometric primitives (lines, arcs)'
        ]
    },
    
    '📐 ANALYSIS TOOLS': {
        'files': ['analysis/spatial_analysis.py'],
        'capabilities': [
            'Room area and volume calculations',
            'Boundary analysis and geometry',
            'Area schemes and spatial elements',
            'Quantity takeoffs and measurements'
        ]
    },
    
    '📋 DOCUMENTATION': {
        'files': ['documentation/schedules_sheets.py'],
        'capabilities': [
            'Create room/door/wall schedules',
            'Material takeoffs and quantity schedules',
            'Create drawing sheets with titleblocks',
            'Place views on sheets with viewports'
        ]
    }
}

# WORKFLOW-BASED INDEX
WORKFLOW_INDEX = {
    '📊 AREA & QUANTITY ANALYSIS': {
        'primary_files': ['analysis/spatial_analysis.py'],
        'supporting_files': ['builtin_elements.py'],
        'use_cases': [
            'Calculate room areas and volumes',
            'Generate area plans and schemes', 
            'Analyze spatial boundaries',
            'Create quantity takeoffs',
            'Room finish schedules',
            'Space programming validation'
        ],
        'key_classes': ['Room', 'Area', 'AreaScheme', 'SpatialElement'],
        'key_parameters': ['ROOM_AREA', 'ROOM_VOLUME', 'AREA_AREA', 'ROOM_PERIMETER']
    },
    
    '📋 SCHEDULE CREATION': {
        'primary_files': ['documentation/schedules_sheets.py'],
        'supporting_files': ['builtin_elements.py', 'selection/selection.py'],
        'use_cases': [
            'Room schedules with areas',
            'Door and window schedules',
            'Wall quantities and areas',
            'Material takeoffs',
            'Equipment schedules',
            'Custom parameter schedules'
        ],
        'key_classes': ['ViewSchedule', 'ScheduleDefinition', 'ScheduleField'],
        'key_methods': ['CreateSchedule', 'AddField', 'AddFilter', 'AddSortGroupField']
    },
    
    '📑 SHEET CREATION': {
        'primary_files': ['documentation/schedules_sheets.py'],
        'supporting_files': ['core/document.py'],
        'use_cases': [
            'Create plan sheets',
            'Create section sheets',
            'Place multiple views on sheets',
            'Organize viewports',
            'Create drawing sets',
            'Sheet numbering and naming'
        ],
        'key_classes': ['ViewSheet', 'Viewport', 'ViewSheetSet'],
        'key_methods': ['Create', 'CanViewBePlaced', 'SetBoxCenter']
    }
}

# COMPLEXITY LEVELS
COMPLEXITY_LEVELS = {
    '🟢 BEGINNER': {
        'recommended_start': ['quick_reference.py', 'core/document.py'],
        'topics': [
            'Getting active document',
            'Basic element selection',
            'Simple transactions',
            'Reading element parameters'
        ]
    },
    
    '🟡 INTERMEDIATE': {
        'recommended_files': ['selection/selection.py', 'elements/creation.py'],
        'topics': [
            'FilteredElementCollector usage',
            'Creating basic elements',
            'Parameter modification',
            'Simple analysis operations'
        ]
    },
    
    '🔴 ADVANCED': {
        'recommended_files': ['analysis/spatial_analysis.py', 'documentation/schedules_sheets.py'],
        'topics': [
            'Complex spatial analysis',
            'Schedule creation and management',
            'Sheet creation workflows',
            'Transaction groups and error handling'
        ]
    }
}

# QUICK START GUIDE
QUICK_START_PATHS = {
    'I want to analyze room areas': 'Start with analysis/spatial_analysis.py',
    'I want to create schedules': 'Start with documentation/schedules_sheets.py',
    'I want to create elements': 'Start with elements/creation.py',
    'I want to select elements': 'Start with selection/selection.py',
    'I need parameter reference': 'Start with builtin_elements.py',
    'I want complete examples': 'Start with examples/complete_workflows.py'
}
