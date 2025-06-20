# Commit Changes

Create semantic commits with proper messages, emoji, and conventional commit format.

## Usage:
`/project:commit-changes [commit-type] [description]`

## Process:
1. **Analyze Changes**: Review all staged and unstaged changes
2. **Determine Commit Type**: Identify the type of changes (feat, fix, docs, etc.)
3. **Generate Message**: Create conventional commit message with emoji
4. **Validate Changes**: Ensure changes are logical and complete
5. **Stage Files**: Add appropriate files to staging area
6. **Create Commit**: Execute git commit with generated message
7. **Suggest Next Steps**: Recommend push, PR creation, or additional work

## Commit Types:
- **feat**: ✨ New feature or enhancement
- **fix**: 🐛 Bug fix
- **docs**: 📚 Documentation changes
- **style**: 💄 Code style/formatting changes
- **refactor**: ♻️ Code refactoring without behavior change
- **test**: 🧪 Adding or updating tests
- **chore**: 🔧 Build process or auxiliary tool changes
- **perf**: ⚡ Performance improvements
- **ci**: 👷 CI/CD configuration changes
- **build**: 📦 Build system or dependencies

## Message Format:
```
<type>(<scope>): <emoji> <description>

<optional body>

<optional footer>
```

## Examples:
- `/project:commit-changes feat "Add user authentication system"`
- `/project:commit-changes fix "Resolve login validation bug"`
- `/project:commit-changes` - Auto-detect commit type and generate message

## Smart Detection:
- Analyze file changes to suggest commit type
- Detect breaking changes and add BREAKING CHANGE footer
- Identify scope from modified files (api, auth, ui, etc.)
- Suggest co-authors from git log

## Output:
- Generated commit message preview
- List of files to be committed
- Suggested next actions (push, create PR, etc.)

## Notes:
- Follows Conventional Commits specification
- Integrates with GitHub for automatic changelog generation
- Can be used with git hooks for automatic message generation