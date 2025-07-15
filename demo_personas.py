#!/usr/bin/env python3
"""
Demo script for the Persona System

This script demonstrates how to use the persona system to direct Claude's
behavior for different specialized tasks.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from persona_system import persona_manager, command_handler, PersonaType


def demo_separator(title: str):
    """Print a demo section separator."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def demo_list_personas():
    """Demo listing all available personas."""
    demo_separator("📋 LIST ALL PERSONAS")
    result = command_handler.handle_list_command()
    print(result)


def demo_activate_persona():
    """Demo activating different personas."""
    demo_separator("🟢 ACTIVATE PERSONA")
    
    # Activate data scientist persona
    print("Activating Data Scientist persona...")
    result = command_handler.handle_activate_command("data-scientist")
    print(result)
    
    print("\n" + "-"*40)
    
    # Show current status
    print("Current persona status:")
    active = persona_manager.get_active_persona()
    if active:
        print(f"Active: {active.name}")
        print(f"Focus: {active.description}")
    
    print("\n" + "-"*40)
    
    # Activate security engineer persona
    print("Switching to Security Engineer persona...")
    result = command_handler.handle_activate_command("security-engineer")
    print(result)


def demo_persona_info():
    """Demo getting detailed persona information."""
    demo_separator("ℹ️  PERSONA INFORMATION")
    
    personas_to_show = ["data-scientist", "security-engineer", "devops-engineer"]
    
    for persona in personas_to_show:
        print(f"\n--- {persona.upper()} INFO ---")
        result = command_handler.handle_info_command(persona)
        print(result)
        if persona != personas_to_show[-1]:  # Not the last one
            print("\n" + "-"*40)


def demo_suggest_personas():
    """Demo getting persona suggestions for different contexts."""
    demo_separator("💡 PERSONA SUGGESTIONS")
    
    contexts = [
        "machine learning model development",
        "api security review",
        "performance optimization",
        "ci/cd pipeline setup",
        "data analysis and visualization"
    ]
    
    for context in contexts:
        print(f"\nContext: '{context}'")
        result = command_handler.handle_suggest_command(context)
        print(result)
        print("-" * 40)


def demo_deactivate_persona():
    """Demo deactivating current persona."""
    demo_separator("⚪ DEACTIVATE PERSONA")
    
    # Show current status
    active = persona_manager.get_active_persona()
    if active:
        print(f"Currently active: {active.name}")
    
    # Deactivate
    result = command_handler.handle_deactivate_command()
    print(result)
    
    # Show new status
    active = persona_manager.get_active_persona()
    if active:
        print(f"Still active: {active.name}")
    else:
        print("No persona is currently active (default mode)")


def demo_persona_specializations():
    """Demo showing persona command specializations."""
    demo_separator("🎯 PERSONA SPECIALIZATIONS")
    
    print("Command specializations by persona:\n")
    
    for persona_type, config in persona_manager.personas.items():
        print(f"**{config.name}**:")
        for cmd in config.command_specializations:
            print(f"  • {cmd}")
        print()


def demo_context_triggers():
    """Demo showing context-based persona activation."""
    demo_separator("🔄 CONTEXT TRIGGERS")
    
    print("Keywords that trigger persona suggestions:\n")
    
    trigger_examples = {
        "Data Science": ["data", "ml", "model", "statistics", "experiment"],
        "Security": ["security", "vulnerability", "auth", "compliance"],
        "DevOps": ["deployment", "ci/cd", "docker", "kubernetes", "monitoring"],
        "Performance": ["performance", "optimization", "load", "scaling"],
        "API/Integration": ["api", "integration", "services", "microservices"]
    }
    
    for category, triggers in trigger_examples.items():
        print(f"**{category}**: {', '.join(triggers)}")
    
    print("\nExample usage:")
    print("If you mention 'docker deployment', it will suggest DevOps Engineer")
    print("If you mention 'model training', it will suggest Data Scientist")


def demo_workflow_example():
    """Demo a complete workflow using personas."""
    demo_separator("🔄 WORKFLOW EXAMPLE")
    
    print("Simulating a complete development workflow with personas:\n")
    
    # Step 1: Planning
    print("1. PROJECT PLANNING PHASE")
    print("   Context: 'system architecture for ML platform'")
    result = command_handler.handle_suggest_command("system architecture for ML platform")
    print(f"   {result}")
    
    print("\n   → Activating Architect persona for system design")
    result = command_handler.handle_activate_command("architect")
    print(f"   {result}")
    
    # Step 2: Development
    print("\n2. DEVELOPMENT PHASE")
    print("   Switching to Developer persona for implementation")
    result = command_handler.handle_activate_command("developer")
    print(f"   {result}")
    
    # Step 3: ML Development
    print("\n3. ML MODEL DEVELOPMENT")
    print("   Switching to Data Scientist persona for ML work")
    result = command_handler.handle_activate_command("data-scientist")
    print(f"   {result}")
    
    # Step 4: Security Review
    print("\n4. SECURITY REVIEW PHASE")
    print("   Switching to Security Engineer persona for security audit")
    result = command_handler.handle_activate_command("security-engineer")
    print(f"   {result}")
    
    # Step 5: Deployment
    print("\n5. DEPLOYMENT PHASE")
    print("   Switching to DevOps Engineer persona for deployment")
    result = command_handler.handle_activate_command("devops-engineer")
    print(f"   {result}")
    
    # Step 6: Performance Testing
    print("\n6. PERFORMANCE TESTING")
    print("   Switching to Performance Engineer persona for optimization")
    result = command_handler.handle_activate_command("performance-engineer")
    print(f"   {result}")
    
    # Step 7: Final Review
    print("\n7. FINAL REVIEW")
    print("   Deactivating persona for general review")
    result = command_handler.handle_deactivate_command()
    print(f"   {result}")


def main():
    """Run the complete persona system demo."""
    print("🎭 PERSONA SYSTEM DEMO")
    print("This demo shows how to use personas to direct Claude's behavior")
    print("for specialized tasks like data science, security, DevOps, etc.")
    
    # Run all demos
    demo_list_personas()
    demo_activate_persona()
    demo_persona_info()
    demo_suggest_personas()
    demo_deactivate_persona()
    demo_persona_specializations()
    demo_context_triggers()
    demo_workflow_example()
    
    # Final summary
    demo_separator("✅ DEMO COMPLETE")
    print("The persona system provides:")
    print("• 9 specialized expert personas")
    print("• Context-aware suggestions")
    print("• Command specializations")
    print("• Seamless activation/deactivation")
    print("• Integration with existing command system")
    print("\nTo use in Claude Code:")
    print("• /personas:list - Show all personas")
    print("• /personas:activate <name> - Activate a persona")
    print("• /personas:info <name> - Get persona details")
    print("• /personas:suggest <context> - Get suggestions")
    print("• /personas:deactivate - Return to default mode")


if __name__ == "__main__":
    main()