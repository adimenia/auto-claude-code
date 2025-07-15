"""
Persona System for Claude Code Integration

This module provides functionality to manage and activate different personas
that direct Claude's behavior for specialized tasks like data science, 
backend engineering, security, etc.
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum


class PersonaType(str, Enum):
    """Available persona types."""
    ARCHITECT = "architect"
    DATA_SCIENTIST = "data-scientist"
    DEVELOPER = "developer"
    DEVOPS_ENGINEER = "devops-engineer"
    INTEGRATION_SPECIALIST = "integration-specialist"
    PERFORMANCE_ENGINEER = "performance-engineer"
    PRODUCT_MANAGER = "product-manager"
    SECURITY_ENGINEER = "security-engineer"
    TESTER = "tester"


@dataclass
class PersonaConfig:
    """Configuration for a persona."""
    name: str
    type: PersonaType
    description: str
    focus_areas: List[str]
    responsibilities: List[str]
    activation_triggers: List[str]
    command_specializations: List[str]
    template_path: str
    is_active: bool = False


class PersonaManager:
    """Manages persona loading, activation, and command integration."""
    
    def __init__(self, templates_path: str = "templates/personas"):
        self.templates_path = Path(templates_path)
        self.personas: Dict[PersonaType, PersonaConfig] = {}
        self.active_persona: Optional[PersonaType] = None
        self._load_personas()
    
    def _load_personas(self) -> None:
        """Load all persona configurations from template files."""
        persona_definitions = {
            PersonaType.ARCHITECT: {
                "name": "Architect",
                "description": "System design, scalability, and technical architecture",
                "focus_areas": [
                    "System Design", "Scalability Planning", "Technology Selection",
                    "Integration Patterns", "Performance Architecture", "Future-Proofing"
                ],
                "responsibilities": [
                    "Overall architecture patterns and design decisions",
                    "Horizontal and vertical scaling strategies",
                    "Framework and tool recommendations",
                    "Service communication and data flow design",
                    "System-level performance considerations",
                    "Extensibility and maintainability planning"
                ],
                "activation_triggers": ["architecture", "design", "scalability", "system"],
                "command_specializations": ["api-design", "performance-audit", "containerize"]
            },
            PersonaType.DATA_SCIENTIST: {
                "name": "Data Scientist",
                "description": "ML models, data quality, and statistical rigor",
                "focus_areas": [
                    "Data Quality & Integrity", "Statistical Rigor", "Model Performance",
                    "Reproducibility", "Feature Engineering", "Ethical AI & Bias",
                    "Experiment Design", "Model Interpretability"
                ],
                "responsibilities": [
                    "Data validation, cleaning, and bias detection",
                    "Hypothesis testing, significance analysis, and methodology",
                    "Model evaluation, validation, and performance metrics",
                    "Experiment tracking, version control, and documentation",
                    "Feature selection, transformation, and domain knowledge",
                    "Fairness, bias detection, and responsible AI practices",
                    "A/B testing, statistical power, and experimental methodology",
                    "Explainable AI and model transparency"
                ],
                "activation_triggers": ["data", "ml", "model", "statistics", "experiment"],
                "command_specializations": ["data-exploration", "model-development", "experiment-tracking", "data-pipeline"]
            },
            PersonaType.DEVELOPER: {
                "name": "Developer",
                "description": "Code quality, patterns, and implementation best practices",
                "focus_areas": [
                    "Code Quality", "Design Patterns", "Testing Strategy",
                    "Documentation", "Refactoring", "Standards Compliance"
                ],
                "responsibilities": [
                    "Clean code principles and maintainability",
                    "Appropriate pattern usage and implementation",
                    "Unit testing, TDD, and test coverage",
                    "Code documentation and API design",
                    "Code improvement and technical debt reduction",
                    "Coding standards and style guidelines"
                ],
                "activation_triggers": ["code", "development", "testing", "patterns"],
                "command_specializations": ["create-feature", "integration-test", "check-all"]
            },
            PersonaType.DEVOPS_ENGINEER: {
                "name": "DevOps Engineer",
                "description": "CI/CD, deployment, infrastructure, and monitoring",
                "focus_areas": [
                    "Deployment Strategy", "Infrastructure as Code", "Containerization",
                    "Monitoring & Logging", "Scalability", "Environment Configuration",
                    "Backup & Recovery"
                ],
                "responsibilities": [
                    "CI/CD pipeline design and automation",
                    "Terraform, CloudFormation, and configuration management",
                    "Docker, Kubernetes, and orchestration",
                    "Application monitoring, alerting, and observability",
                    "Auto-scaling, load balancing, and performance optimization",
                    "Development, staging, and production environments",
                    "Disaster recovery and business continuity planning"
                ],
                "activation_triggers": ["deployment", "ci/cd", "docker", "kubernetes", "monitoring"],
                "command_specializations": ["setup-ci", "containerize", "deploy-config"]
            },
            PersonaType.INTEGRATION_SPECIALIST: {
                "name": "Integration Specialist",
                "description": "API design, service integration, and data flow",
                "focus_areas": [
                    "API Design", "Data Flow", "Error Propagation",
                    "Service Contracts", "Integration Testing", "Rate Limiting",
                    "Circuit Breakers", "Message Formats"
                ],
                "responsibilities": [
                    "RESTful API design and GraphQL implementation",
                    "Inter-service communication and data consistency",
                    "Distributed system error handling",
                    "API versioning and backward compatibility",
                    "Service integration and contract testing",
                    "API throttling and usage control",
                    "Fault tolerance and resilience patterns",
                    "Data serialization and protocol design"
                ],
                "activation_triggers": ["api", "integration", "services", "microservices"],
                "command_specializations": ["api-design", "integration-test", "data-migration"]
            },
            PersonaType.PERFORMANCE_ENGINEER: {
                "name": "Performance Engineer",
                "description": "Optimization, load testing, and scalability",
                "focus_areas": [
                    "Performance Bottlenecks", "Resource Utilization", "Database Optimization",
                    "Caching Strategy", "Asynchronous Processing", "Load Testing Readiness",
                    "Scalability Patterns", "Profiling Integration"
                ],
                "responsibilities": [
                    "Identification and resolution of performance issues",
                    "CPU, memory, and I/O optimization",
                    "Query performance and indexing strategies",
                    "Application and database caching implementation",
                    "Background jobs and async operation design",
                    "Performance testing and capacity planning",
                    "Horizontal scaling and performance architecture",
                    "Performance monitoring and profiling tools"
                ],
                "activation_triggers": ["performance", "optimization", "load", "scaling"],
                "command_specializations": ["performance-audit", "load-test"]
            },
            PersonaType.PRODUCT_MANAGER: {
                "name": "Product Manager",
                "description": "UX, business logic, and feature completeness",
                "focus_areas": [
                    "User Experience", "Feature Completeness", "Business Logic",
                    "Error Handling UX", "Accessibility", "Performance Impact",
                    "Data Analytics", "Edge Cases"
                ],
                "responsibilities": [
                    "User journey optimization and usability",
                    "Business requirement validation and feature gaps",
                    "Requirement translation and business rule implementation",
                    "User-friendly error messages and recovery flows",
                    "WCAG compliance and inclusive design",
                    "User-perceived performance and experience optimization",
                    "User behavior tracking and analytics implementation",
                    "User scenario validation and edge case handling"
                ],
                "activation_triggers": ["ux", "business", "user", "requirements"],
                "command_specializations": ["analyze-requirements", "create-docs"]
            },
            PersonaType.SECURITY_ENGINEER: {
                "name": "Security Engineer",
                "description": "Vulnerability assessment, security auditing, and compliance",
                "focus_areas": [
                    "Vulnerability Assessment", "Authentication & Authorization", "Data Protection",
                    "Input Validation", "Security Configuration", "Dependency Security",
                    "Secrets Management", "Compliance"
                ],
                "responsibilities": [
                    "Security threat analysis and OWASP compliance",
                    "Secure access control implementation",
                    "Encryption, data privacy, and secure storage",
                    "SQL injection, XSS, and input sanitization",
                    "Secure headers, HTTPS, and security policies",
                    "Third-party library vulnerability scanning",
                    "Secure credential and API key handling",
                    "GDPR, HIPAA, and regulatory requirement adherence"
                ],
                "activation_triggers": ["security", "vulnerability", "auth", "compliance"],
                "command_specializations": ["security-audit", "secrets-scan", "security-headers"]
            },
            PersonaType.TESTER: {
                "name": "Tester",
                "description": "Testing strategies, quality assurance, and validation",
                "focus_areas": [
                    "Test Coverage", "Quality Assurance", "Test Automation",
                    "Edge Case Testing", "Performance Testing", "User Acceptance"
                ],
                "responsibilities": [
                    "Comprehensive testing strategy and coverage analysis",
                    "Bug prevention and quality gates",
                    "Automated testing frameworks and CI integration",
                    "Boundary conditions and error scenarios",
                    "Load testing and performance validation",
                    "End-to-end testing and user journey validation"
                ],
                "activation_triggers": ["test", "quality", "qa", "validation"],
                "command_specializations": ["integration-test", "load-test", "check-all"]
            }
        }
        
        for persona_type, config in persona_definitions.items():
            template_path = self.templates_path / f"{persona_type.value}.md"
            self.personas[persona_type] = PersonaConfig(
                name=config["name"],
                type=persona_type,
                description=config["description"],
                focus_areas=config["focus_areas"],
                responsibilities=config["responsibilities"],
                activation_triggers=config["activation_triggers"],
                command_specializations=config["command_specializations"],
                template_path=str(template_path)
            )
    
    def list_personas(self) -> List[PersonaConfig]:
        """Get list of all available personas."""
        return list(self.personas.values())
    
    def get_persona(self, persona_type: PersonaType) -> Optional[PersonaConfig]:
        """Get specific persona configuration."""
        return self.personas.get(persona_type)
    
    def activate_persona(self, persona_type: PersonaType) -> bool:
        """Activate a specific persona."""
        if persona_type not in self.personas:
            return False
        
        # Deactivate current persona
        if self.active_persona:
            self.personas[self.active_persona].is_active = False
        
        # Activate new persona
        self.personas[persona_type].is_active = True
        self.active_persona = persona_type
        return True
    
    def deactivate_persona(self) -> bool:
        """Deactivate current persona."""
        if not self.active_persona:
            return False
        
        self.personas[self.active_persona].is_active = False
        self.active_persona = None
        return True
    
    def get_active_persona(self) -> Optional[PersonaConfig]:
        """Get currently active persona."""
        if self.active_persona:
            return self.personas[self.active_persona]
        return None
    
    def suggest_persona_for_command(self, command: str) -> List[PersonaType]:
        """Suggest personas based on command."""
        suggestions = []
        for persona_type, config in self.personas.items():
            if command in config.command_specializations:
                suggestions.append(persona_type)
        return suggestions
    
    def suggest_persona_for_context(self, context: str) -> List[PersonaType]:
        """Suggest personas based on context keywords."""
        suggestions = []
        context_lower = context.lower()
        
        for persona_type, config in self.personas.items():
            for trigger in config.activation_triggers:
                if trigger in context_lower:
                    suggestions.append(persona_type)
                    break
        
        return suggestions
    
    def get_persona_template(self, persona_type: PersonaType) -> Optional[str]:
        """Get persona template content."""
        if persona_type not in self.personas:
            return None
        
        template_path = Path(self.personas[persona_type].template_path)
        if template_path.exists():
            return template_path.read_text()
        return None
    
    def export_persona_config(self, persona_type: PersonaType) -> Optional[Dict[str, Any]]:
        """Export persona configuration as dictionary."""
        if persona_type not in self.personas:
            return None
        return asdict(self.personas[persona_type])
    
    def export_all_personas(self) -> Dict[str, Any]:
        """Export all persona configurations."""
        return {
            persona_type.value: asdict(config)
            for persona_type, config in self.personas.items()
        }


class PersonaCommandHandler:
    """Handles persona-related commands."""
    
    def __init__(self, persona_manager: PersonaManager):
        self.persona_manager = persona_manager
    
    def handle_list_command(self) -> str:
        """Handle /personas:list command."""
        personas = self.persona_manager.list_personas()
        active_persona = self.persona_manager.get_active_persona()
        
        output = ["Available Personas:\n"]
        
        for persona in personas:
            status = "🟢 ACTIVE" if persona.is_active else "⚪ Available"
            output.append(f"{status} {persona.name}")
            output.append(f"   Type: {persona.type.value}")
            output.append(f"   Description: {persona.description}")
            output.append(f"   Specializations: {', '.join(persona.command_specializations[:3])}")
            output.append("")
        
        if active_persona:
            output.append(f"Currently Active: {active_persona.name}")
        else:
            output.append("No persona currently active")
        
        return "\n".join(output)
    
    def handle_activate_command(self, persona_name: str) -> str:
        """Handle /personas:activate command."""
        # Map persona name to type
        persona_type = None
        for ptype, config in self.persona_manager.personas.items():
            if config.name.lower() == persona_name.lower() or ptype.value == persona_name.lower():
                persona_type = ptype
                break
        
        if not persona_type:
            return f"Persona '{persona_name}' not found. Use /personas:list to see available personas."
        
        if self.persona_manager.activate_persona(persona_type):
            persona = self.persona_manager.get_persona(persona_type)
            return f"✅ Activated {persona.name} persona\n\nFocus: {persona.description}\n\nKey Areas: {', '.join(persona.focus_areas[:4])}"
        else:
            return f"Failed to activate persona '{persona_name}'"
    
    def handle_deactivate_command(self) -> str:
        """Handle /personas:deactivate command."""
        active_persona = self.persona_manager.get_active_persona()
        if not active_persona:
            return "No persona is currently active."
        
        if self.persona_manager.deactivate_persona():
            return f"✅ Deactivated {active_persona.name} persona"
        else:
            return "Failed to deactivate persona"
    
    def handle_suggest_command(self, context: str) -> str:
        """Handle /personas:suggest command."""
        suggestions = self.persona_manager.suggest_persona_for_context(context)
        
        if not suggestions:
            return f"No persona suggestions found for context: '{context}'"
        
        output = [f"Suggested personas for '{context}':\n"]
        
        for persona_type in suggestions:
            persona = self.persona_manager.get_persona(persona_type)
            output.append(f"• {persona.name} - {persona.description}")
        
        return "\n".join(output)
    
    def handle_info_command(self, persona_name: str) -> str:
        """Handle /personas:info command."""
        persona_type = None
        for ptype, config in self.persona_manager.personas.items():
            if config.name.lower() == persona_name.lower() or ptype.value == persona_name.lower():
                persona_type = ptype
                break
        
        if not persona_type:
            return f"Persona '{persona_name}' not found."
        
        persona = self.persona_manager.get_persona(persona_type)
        output = [
            f"# {persona.name} Persona",
            f"**Description:** {persona.description}",
            "",
            "## Focus Areas:",
            *[f"• {area}" for area in persona.focus_areas],
            "",
            "## Key Responsibilities:",
            *[f"• {resp}" for resp in persona.responsibilities[:5]],
            "",
            "## Command Specializations:",
            *[f"• {cmd}" for cmd in persona.command_specializations],
            "",
            "## Activation Triggers:",
            *[f"• {trigger}" for trigger in persona.activation_triggers]
        ]
        
        return "\n".join(output)


# Global persona manager instance
persona_manager = PersonaManager()
command_handler = PersonaCommandHandler(persona_manager)