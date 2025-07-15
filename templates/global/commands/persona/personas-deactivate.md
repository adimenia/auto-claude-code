# Personas Deactivate Command

## Command Overview
Deactivate the currently active persona, returning Claude to default behavior.

## Usage
```
/personas:deactivate
```

## Implementation

### Python Implementation
```python
from src.persona_system import persona_manager, command_handler

# Deactivate current persona
result = command_handler.handle_deactivate_command()
print(result)
```

## Expected Output

### Successful Deactivation
```
✅ Deactivated Data Scientist persona
```

### No Active Persona
```
No persona is currently active.
```

## Behavior Changes

### After Deactivation
Claude returns to default behavior:
- **General Purpose**: No specialized focus or bias
- **Balanced Analysis**: Equal weight to all aspects of code/system
- **Comprehensive Coverage**: Considers all areas without specialization
- **Neutral Perspective**: No domain-specific expertise emphasis
- **Standard Recommendations**: General best practices without specialty focus

### Before Deactivation (Example: Data Scientist Active)
Claude was focused on:
- Data quality and statistical rigor
- Model performance and validation
- Reproducibility and experiment tracking
- Feature engineering and ethical AI
- ML-specific patterns and practices

### After Deactivation
Claude provides:
- General code quality assessment
- Standard software engineering practices
- Balanced security, performance, and maintainability considerations
- Generic best practices across all domains
- No specialized domain expertise

## Use Cases

### When to Deactivate
1. **Task Completion**: After finishing specialized work
2. **Context Switch**: Before switching to different type of work
3. **General Review**: When you want unbiased, general analysis
4. **Exploration**: When exploring code without specific focus
5. **Troubleshooting**: When specialized persona isn't helpful

### Example Workflow
```bash
# Start with data science work
/personas:activate data-scientist
# ... work on ML models, data analysis ...

# Switch to general development
/personas:deactivate
# ... work on general application features ...

# Switch to security focus
/personas:activate security-engineer
# ... security review and hardening ...

# Return to general mode
/personas:deactivate
```

## Features
- **Immediate Effect**: Persona is deactivated immediately
- **State Reset**: Returns to neutral, non-specialized state
- **Error Handling**: Clear message when no persona is active
- **Status Update**: Confirms which persona was deactivated
- **Clean Transition**: Smooth transition back to default behavior

## Integration Notes
- Works with any currently active persona
- No parameters required
- Safe to call multiple times
- Integrates with persona management system
- Preserves persona definitions for future activation

## Related Commands
- `/personas:list` - See all available personas and current status
- `/personas:activate <persona>` - Activate a specific persona
- `/personas:info <persona>` - Get detailed persona information
- `/personas:suggest <context>` - Get persona suggestions

## Best Practices
1. **Clean Transitions**: Deactivate when switching work contexts
2. **General Reviews**: Use default state for unbiased analysis
3. **Debugging**: Try deactivating if persona isn't helpful
4. **Documentation**: Deactivate for general documentation tasks
5. **Code Exploration**: Use default state when exploring unfamiliar code