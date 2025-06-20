# Analyze Requirements

Break down complex requirements into actionable tasks with clear acceptance criteria.

## Usage:
`/project:analyze-requirements [requirement-description]`

## Process:
1. **Requirement Parsing**: Extract key requirements from $ARGUMENTS
2. **Stakeholder Analysis**: Identify who will be affected by the changes
3. **Technical Analysis**: Assess technical complexity and dependencies
4. **Task Breakdown**: Create specific, measurable, actionable tasks
5. **Acceptance Criteria**: Define clear success criteria for each task
6. **Risk Assessment**: Identify potential risks and mitigation strategies
7. **Estimation**: Provide effort estimates and timeline suggestions
8. **Documentation**: Create structured requirement document

## Output Structure:
```markdown
# Requirement Analysis: [Feature Name]

## Overview
Brief description of the requirement and its business value.

## Stakeholders
- Primary: [Who directly benefits]
- Secondary: [Who is indirectly affected]
- Technical: [Who implements/maintains]

## Technical Requirements
- Functional requirements
- Non-functional requirements (performance, security, etc.)
- Integration requirements
- Data requirements

## Task Breakdown
1. **Task 1**: Description
   - Acceptance Criteria: [Specific, testable criteria]
   - Effort: [S/M/L or hours]
   - Dependencies: [What must be done first]

2. **Task 2**: Description
   - [Same structure as above]

## Risk Analysis
- **High Risk**: [Critical risks with mitigation plans]
- **Medium Risk**: [Moderate risks to monitor]
- **Low Risk**: [Minor risks for awareness]

## Definition of Done
- [ ] All acceptance criteria met
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Code reviewed and approved
- [ ] Deployed to staging
- [ ] Stakeholder sign-off received
```

## Examples:
- `/project:analyze-requirements "Add two-factor authentication to user login"`
- `/project:analyze-requirements "Create data export feature for analytics dashboard"`
- `/project:analyze-requirements "Optimize database queries for user search"`

## Analysis Framework:
- **SMART Criteria**: Specific, Measurable, Achievable, Relevant, Time-bound
- **MoSCoW Prioritization**: Must have, Should have, Could have, Won't have
- **User Story Format**: As a [user], I want [goal] so that [benefit]

## Notes:
- Include non-functional requirements (performance, security, usability)
- Consider edge cases and error scenarios
- Align with existing system architecture
- Involve relevant stakeholders in validation