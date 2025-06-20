# Cleanup Code

Remove dead code, unused imports, optimize structure, and improve code quality.

## Usage:
`/project:cleanup-code [--scope] [--aggressive]` or `/user:cleanup-code [--scope]`

## Process:
1. **Dead Code Detection**: Identify unused functions, classes, and variables
2. **Import Optimization**: Remove unused imports and organize them
3. **Code Deduplication**: Find and consolidate duplicate code
4. **Formatting Consistency**: Apply consistent code formatting
5. **Structure Optimization**: Improve file and directory organization
6. **Comment Cleanup**: Remove outdated comments, improve documentation
7. **Performance Optimization**: Basic performance improvements
8. **Dependency Cleanup**: Remove unused dependencies

## Scope Options:
- `--current-file`: Clean only the current file
- `--directory [path]`: Clean specific directory
- `--module [name]`: Clean specific module
- `--all`: Clean entire project (default)

## Cleanup Categories:
- **Imports**: Unused imports, duplicate imports, import ordering
- **Variables**: Unused variables, redundant assignments
- **Functions**: Unused functions, duplicate functions
- **Classes**: Unused classes, empty classes
- **Files**: Empty files, duplicate files
- **Dependencies**: Unused packages in requirements

## Framework-Specific Cleanup:
- **Python**: Remove unused imports, variables, functions; optimize imports with isort
- **JavaScript**: Remove unused variables, dead code elimination
- **FastAPI**: Remove unused routes, optimize dependency injection
- **Django**: Remove unused models, views, cleanup migrations
- **Data Science**: Remove unused notebooks, optimize data processing

## Safety Measures:
- Create backup before major changes
- Preserve public APIs and interfaces
- Maintain test coverage
- Check for dynamic imports/references
- Validate after cleanup

## Examples:
- `/project:cleanup-code` - Clean entire project safely
- `/project:cleanup-code --scope current-file` - Clean current file only
- `/project:cleanup-code --aggressive` - More thorough cleanup (higher risk)

## Output:
- Summary of changes made
- List of files modified
- Potential issues requiring manual review
- Backup location (if created)

## Notes:
- Always run tests after cleanup
- Review changes before committing
- Use --aggressive flag cautiously
- Some cleanup may require manual verification