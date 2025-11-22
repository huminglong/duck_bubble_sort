# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Chinese educational visualization project that demonstrates the bubble sort algorithm using animated ducks. The application uses Python + Tkinter to create an interactive sorting visualization where 12 baby ducks of different sizes are sorted by a mother duck character.

## Running the Application

### Primary Methods

1. **Using the startup script (Recommended)**:
   ```bash
   python duck_bubble_sort/run.py
   ```

2. **Direct execution of main program**:
   ```bash
   python duck_bubble_sort/main.py
   ```

3. **As a module**:
   ```bash
   python -m duck_bubble_sort.main
   ```

The startup script (`run.py`) performs environment checks, validates project structure, and handles initialization before launching the main application.

## System Requirements

- **Python**: 3.6+ (required)
- **Dependencies**: Only Python standard libraries (tkinter, random, threading, time, math, typing)
- **No external packages** required

## Project Architecture

The codebase follows a modular MVC-like architecture with the following key components:

### Core Modules

1. **Main Application** (`main.py`): Contains `DuckBubbleSortApp` - the main GUI controller
2. **Graphics System** (`graphics.py`): Duck rendering classes (`BabyDuck`, `MotherDuck`, `DuckFactory`)
3. **Algorithm Module** (`algorithms/bubble_sort.py`): Bubble sort implementation with animation callbacks
4. **Animation System** (`animation/`):
   - `animation_engine.py`: Core animation engine
   - `animators.py`: Specialized animation classes
   - `sort_animation_integration.py`: Bridge between algorithm and animation

### Key Design Patterns

- **Factory Pattern**: `DuckFactory` creates duck objects with appropriate sizing
- **Observer Pattern**: Sorting algorithm notifies animation system via callbacks
- **Threading**: Animations run in separate threads for smooth performance
- **State Management**: Comprehensive state tracking for sorting, animation, and UI

## Duck Visual System

- **Baby Ducks**: Represent array elements, size varies by value (20-50px)
- **Mother Duck**: Fixed size (60px), orchestrates the sorting demonstration
- **State Colors**:
  - Default: Golden yellow
  - Highlight: Pink
  - Comparing: Dark cyan
  - Sorted: Green

## Animation Integration

The sorting algorithm uses generators to yield state changes, which trigger corresponding animations:
- Comparison operations → Mother duck moves to compare position
- Swap operations → Ducks exchange positions with arc animations
- Completion → Celebration animations with all ducks turning green

## Testing

No automated test framework is configured. The project includes manual test programs:
- `test_graphics.py`: Graphics rendering tests
- `test_animation.py`: Animation system tests
- `test_bubble_sort.py`: Algorithm logic tests

Run individual test programs directly from the `duck_bubble_sort` directory.

## Common Development Tasks

### Adding New Sorting Algorithms
1. Create algorithm class in `algorithms/` directory
2. Implement generator pattern for step-by-step execution
3. Add corresponding animation integration in `animation/`
4. Update main application to include new algorithm option

### Modifying Duck Appearance
- Edit drawing methods in `graphics.py` (`BabyDuck.draw()` or `MotherDuck.draw()`)
- Adjust color constants in class definitions
- Duck size is automatically calculated based on values for baby ducks

### Animation Adjustments
- Modify animation parameters in `animation_engine.py`
- Add new animation types in `animators.py`
- Update integration logic in `sort_animation_integration.py`

## File Structure Notes

- All core functionality is within the `duck_bubble_sort/` subdirectory
- The project uses only standard Python libraries - no `requirements.txt`
- Configuration is handled through constants in individual modules
- Logging is implemented but basic (see `logger.py` reference in imports)

## Language and Documentation

The project and its documentation are primarily in Chinese. This includes:
- UI text and labels in the application
- README files and documentation
- Code comments and docstrings
- User-facing messages and error text