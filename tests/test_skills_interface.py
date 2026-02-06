"""
Test suite for Skills Interface modules.

Validates that Skills modules accept correct parameters and return data structures
matching the Input/Output contracts defined in:
- skills/README.md
- specs/technical.md

These tests SHOULD FAIL initially (no implementation exists).
This defines the "Empty Slot" that implementation must fill.
"""

import pytest
import uuid
import json
from datetime import datetime
from typing import Dict, Any, List

# These imports will fail until skill modules are implemented
# Expected locations:
# - chimera/skills/perception/monitor_resources.py
# - chimera/skills/content/generate_text.py
# - chimera/skills/social/post_content.py
from chimera.skills.perception.monitor_resources import skill_monitor_resources
from chimera.skills.content.generate_text import skill_generate_text
from chimera.skills.social.post_content import skill_post_content


class TestSkillMonitorResources:
    """Test suite for skill_monitor_resources Input/Output contract."""

    def test_skill_monitor_resources_function_exists(self):
        """Test that skill_monitor_resources function exists and is callable."""
        assert callable(skill_monitor_resources), (
            "skill_monitor_resources function must exist"
        )

    def test_skill_monitor_resources_required_parameters(self):
        """Test that skill_monitor_resources accepts required parameters."""
        agent_id = str(uuid.uuid4())
        resource_uris = ["mcp://twitter/mentions/recent"]

        result = skill_monitor_resources(agent_id=agent_id, resource_uris=resource_uris)

        assert isinstance(result, dict), (
            "skill_monitor_resources must return a dictionary"
        )

    def test_skill_monitor_resources_input_contract(self):
        """Test that skill_monitor_resources accepts correct input types."""
        agent_id = str(uuid.uuid4())
        resource_uris = ["mcp://news/ethiopia/fashion/trends"]
        poll_interval_seconds = 60
        last_poll_timestamp = "2026-02-05T12:00:00.000Z"

        # Should accept all parameters per Input Contract
        result = skill_monitor_resources(
            agent_id=agent_id,
            resource_uris=resource_uris,
            poll_interval_seconds=poll_interval_seconds,
            last_poll_timestamp=last_poll_timestamp,
        )

        assert isinstance(result, dict), "Result must be a dictionary"

    def test_skill_monitor_resources_output_contract(self):
        """Test that skill_monitor_resources returns correct output structure."""
        agent_id = str(uuid.uuid4())
        resource_uris = ["mcp://twitter/mentions/recent"]

        result = skill_monitor_resources(agent_id=agent_id, resource_uris=resource_uris)

        # Required fields per Output Contract
        assert "success" in result, "Output must contain 'success' field"
        assert isinstance(result["success"], bool), "'success' must be a boolean"

        if result["success"]:
            assert "updates" in result, (
                "Output must contain 'updates' field when successful"
            )
            assert isinstance(result["updates"], list), "'updates' must be a list"

            assert "poll_timestamp" in result, (
                "Output must contain 'poll_timestamp' field"
            )
            assert isinstance(result["poll_timestamp"], str), (
                "'poll_timestamp' must be a string (ISO 8601)"
            )

            # Validate update structure
            if len(result["updates"]) > 0:
                update = result["updates"][0]
                assert "resource_uri" in update, (
                    "Update must contain 'resource_uri' field"
                )
                assert "content" in update, "Update must contain 'content' field"
                assert "timestamp" in update, "Update must contain 'timestamp' field"
                assert "change_detected" in update, (
                    "Update must contain 'change_detected' field"
                )
                assert isinstance(update["change_detected"], bool), (
                    "'change_detected' must be a boolean"
                )
        else:
            assert "error" in result, (
                "Output must contain 'error' field when unsuccessful"
            )
            assert isinstance(result["error"], str), "'error' must be a string"

    def test_skill_monitor_resources_agent_id_validation(self):
        """Test that agent_id must be a valid UUID string."""
        invalid_agent_id = "not-a-uuid"
        resource_uris = ["mcp://twitter/mentions/recent"]

        # Should handle invalid UUID gracefully or raise appropriate error
        result = skill_monitor_resources(
            agent_id=invalid_agent_id, resource_uris=resource_uris
        )

        # Either returns error or raises exception
        assert isinstance(result, dict), (
            "Must return a dictionary even with invalid input"
        )

    def test_skill_monitor_resources_resource_uris_validation(self):
        """Test that resource_uris must be a list of strings."""
        agent_id = str(uuid.uuid4())

        # Test with empty list (should be valid)
        result = skill_monitor_resources(agent_id=agent_id, resource_uris=[])

        assert isinstance(result, dict), "Must handle empty resource_uris list"


class TestSkillGenerateText:
    """Test suite for skill_generate_text Input/Output contract."""

    def test_skill_generate_text_function_exists(self):
        """Test that skill_generate_text function exists and is callable."""
        assert callable(skill_generate_text), "skill_generate_text function must exist"

    def test_skill_generate_text_required_parameters(self):
        """Test that skill_generate_text accepts required parameters."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        prompt = "Write a witty caption about summer fashion"
        content_type = "caption"

        result = skill_generate_text(
            agent_id=agent_id, task_id=task_id, prompt=prompt, content_type=content_type
        )

        assert isinstance(result, dict), "skill_generate_text must return a dictionary"

    def test_skill_generate_text_input_contract(self):
        """Test that skill_generate_text accepts correct input types."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        prompt = "Write a script for a fashion video"
        content_type = "script"
        persona_constraints = ["Witty", "Gen-Z slang"]
        max_length = 1000
        temperature = 0.8
        system_context = "You are a fashion influencer..."

        result = skill_generate_text(
            agent_id=agent_id,
            task_id=task_id,
            prompt=prompt,
            content_type=content_type,
            persona_constraints=persona_constraints,
            max_length=max_length,
            temperature=temperature,
            system_context=system_context,
        )

        assert isinstance(result, dict), "Result must be a dictionary"

    def test_skill_generate_text_output_contract(self):
        """Test that skill_generate_text returns correct output structure."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        prompt = "Write a reply to a comment"
        content_type = "reply"

        result = skill_generate_text(
            agent_id=agent_id, task_id=task_id, prompt=prompt, content_type=content_type
        )

        # Required fields per Output Contract
        assert "success" in result, "Output must contain 'success' field"
        assert isinstance(result["success"], bool), "'success' must be a boolean"

        if result["success"]:
            assert "text_content" in result, (
                "Output must contain 'text_content' field when successful"
            )
            assert isinstance(result["text_content"], str), (
                "'text_content' must be a string"
            )

            assert "confidence_score" in result, (
                "Output must contain 'confidence_score' field"
            )
            assert isinstance(result["confidence_score"], (int, float)), (
                "'confidence_score' must be a number"
            )
            assert 0.0 <= result["confidence_score"] <= 1.0, (
                "'confidence_score' must be in range [0.0, 1.0]"
            )

            assert "token_count" in result, "Output must contain 'token_count' field"
            assert isinstance(result["token_count"], int), (
                "'token_count' must be a number"
            )

            assert "generated_at" in result, "Output must contain 'generated_at' field"
            assert isinstance(result["generated_at"], str), (
                "'generated_at' must be a string (ISO 8601)"
            )
        else:
            assert "error" in result, (
                "Output must contain 'error' field when unsuccessful"
            )

    def test_skill_generate_text_content_type_validation(self):
        """Test that content_type must be one of allowed values."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        prompt = "Test prompt"

        valid_types = ["caption", "script", "reply", "post"]

        for content_type in valid_types:
            result = skill_generate_text(
                agent_id=agent_id,
                task_id=task_id,
                prompt=prompt,
                content_type=content_type,
            )
            assert isinstance(result, dict), (
                f"Must handle valid content_type: {content_type}"
            )

    def test_skill_generate_text_temperature_range(self):
        """Test that temperature must be in range [0.0, 1.0]."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        prompt = "Test prompt"
        content_type = "caption"

        # Test valid temperature
        result = skill_generate_text(
            agent_id=agent_id,
            task_id=task_id,
            prompt=prompt,
            content_type=content_type,
            temperature=0.7,
        )

        assert isinstance(result, dict), "Must handle valid temperature value"


class TestSkillPostContent:
    """Test suite for skill_post_content Input/Output contract."""

    def test_skill_post_content_function_exists(self):
        """Test that skill_post_content function exists and is callable."""
        assert callable(skill_post_content), "skill_post_content function must exist"

    def test_skill_post_content_required_parameters(self):
        """Test that skill_post_content accepts required parameters."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        platform = "twitter"
        text_content = "Summer drop is here 🔥"

        result = skill_post_content(
            agent_id=agent_id,
            task_id=task_id,
            platform=platform,
            text_content=text_content,
        )

        assert isinstance(result, dict), "skill_post_content must return a dictionary"

    def test_skill_post_content_input_contract(self):
        """Test that skill_post_content accepts correct input types."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        platform = "instagram"
        text_content = "Check out this new outfit!"
        media_urls = ["https://cdn.example.com/img/abc123.png"]
        disclosure_level = "automated"

        result = skill_post_content(
            agent_id=agent_id,
            task_id=task_id,
            platform=platform,
            text_content=text_content,
            media_urls=media_urls,
            disclosure_level=disclosure_level,
        )

        assert isinstance(result, dict), "Result must be a dictionary"

    def test_skill_post_content_output_contract(self):
        """Test that skill_post_content returns correct output structure."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        platform = "threads"
        text_content = "Excited to share this!"

        result = skill_post_content(
            agent_id=agent_id,
            task_id=task_id,
            platform=platform,
            text_content=text_content,
        )

        # Required fields per Output Contract
        assert "success" in result, "Output must contain 'success' field"
        assert isinstance(result["success"], bool), "'success' must be a boolean"

        if result["success"]:
            assert "post_id" in result, (
                "Output must contain 'post_id' field when successful"
            )
            assert isinstance(result["post_id"], str), "'post_id' must be a string"

            assert "url" in result, "Output must contain 'url' field"
            assert isinstance(result["url"], str), "'url' must be a string"

            assert "platform" in result, "Output must contain 'platform' field"
            assert isinstance(result["platform"], str), "'platform' must be a string"
            assert result["platform"] in ["twitter", "instagram", "threads"], (
                "'platform' must be one of: twitter, instagram, threads"
            )

            assert "published_at" in result, "Output must contain 'published_at' field"
            assert isinstance(result["published_at"], str), (
                "'published_at' must be a string (ISO 8601)"
            )
        else:
            assert "error" in result, (
                "Output must contain 'error' field when unsuccessful"
            )

    def test_skill_post_content_platform_validation(self):
        """Test that platform must be one of allowed values."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        text_content = "Test post"

        valid_platforms = ["twitter", "instagram", "threads"]

        for platform in valid_platforms:
            result = skill_post_content(
                agent_id=agent_id,
                task_id=task_id,
                platform=platform,
                text_content=text_content,
            )
            assert isinstance(result, dict), f"Must handle valid platform: {platform}"

    def test_skill_post_content_disclosure_level_validation(self):
        """Test that disclosure_level must be one of allowed values."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        platform = "twitter"
        text_content = "Test post"

        valid_levels = ["automated", "assisted", "none"]

        for disclosure_level in valid_levels:
            result = skill_post_content(
                agent_id=agent_id,
                task_id=task_id,
                platform=platform,
                text_content=text_content,
                disclosure_level=disclosure_level,
            )
            assert isinstance(result, dict), (
                f"Must handle valid disclosure_level: {disclosure_level}"
            )

    def test_skill_post_content_media_urls_validation(self):
        """Test that media_urls must be a list of strings."""
        agent_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())
        platform = "instagram"
        text_content = "Check this out!"
        media_urls = [
            "https://cdn.example.com/img/1.png",
            "https://cdn.example.com/img/2.png",
        ]

        result = skill_post_content(
            agent_id=agent_id,
            task_id=task_id,
            platform=platform,
            text_content=text_content,
            media_urls=media_urls,
        )

        assert isinstance(result, dict), "Must handle media_urls list"


class TestSkillsInterfaceCommon:
    """Common tests applicable to all skills."""

    def test_all_skills_return_dict(self):
        """Test that all skills return a dictionary."""
        agent_id = str(uuid.uuid4())

        # Test skill_monitor_resources
        result1 = skill_monitor_resources(
            agent_id=agent_id, resource_uris=["mcp://twitter/mentions/recent"]
        )
        assert isinstance(result1, dict), (
            "skill_monitor_resources must return a dictionary"
        )

        # Test skill_generate_text
        result2 = skill_generate_text(
            agent_id=agent_id,
            task_id=str(uuid.uuid4()),
            prompt="Test",
            content_type="caption",
        )
        assert isinstance(result2, dict), "skill_generate_text must return a dictionary"

        # Test skill_post_content
        result3 = skill_post_content(
            agent_id=agent_id,
            task_id=str(uuid.uuid4()),
            platform="twitter",
            text_content="Test",
        )
        assert isinstance(result3, dict), "skill_post_content must return a dictionary"

    def test_all_skills_have_success_field(self):
        """Test that all skills return a 'success' boolean field."""
        agent_id = str(uuid.uuid4())

        results = [
            skill_monitor_resources(
                agent_id=agent_id, resource_uris=["mcp://twitter/mentions/recent"]
            ),
            skill_generate_text(
                agent_id=agent_id,
                task_id=str(uuid.uuid4()),
                prompt="Test",
                content_type="caption",
            ),
            skill_post_content(
                agent_id=agent_id,
                task_id=str(uuid.uuid4()),
                platform="twitter",
                text_content="Test",
            ),
        ]

        for result in results:
            assert "success" in result, "All skills must return 'success' field"
            assert isinstance(result["success"], bool), (
                "'success' field must be a boolean"
            )

    def test_all_skills_handle_errors(self):
        """Test that all skills handle errors gracefully."""
        # Invalid UUID should be handled
        invalid_uuid = "not-a-uuid"

        results = [
            skill_monitor_resources(
                agent_id=invalid_uuid, resource_uris=["mcp://twitter/mentions/recent"]
            ),
            skill_generate_text(
                agent_id=invalid_uuid,
                task_id=str(uuid.uuid4()),
                prompt="Test",
                content_type="caption",
            ),
            skill_post_content(
                agent_id=invalid_uuid,
                task_id=str(uuid.uuid4()),
                platform="twitter",
                text_content="Test",
            ),
        ]

        for result in results:
            assert isinstance(result, dict), (
                "Skills must return a dictionary even on error"
            )
            if not result.get("success", True):
                assert "error" in result, "Failed skills must include 'error' field"

    def test_all_skills_json_serializable(self):
        """Test that all skill outputs are JSON serializable."""
        agent_id = str(uuid.uuid4())

        results = [
            skill_monitor_resources(
                agent_id=agent_id, resource_uris=["mcp://twitter/mentions/recent"]
            ),
            skill_generate_text(
                agent_id=agent_id,
                task_id=str(uuid.uuid4()),
                prompt="Test",
                content_type="caption",
            ),
            skill_post_content(
                agent_id=agent_id,
                task_id=str(uuid.uuid4()),
                platform="twitter",
                text_content="Test",
            ),
        ]

        for result in results:
            # Should not raise exception
            json_str = json.dumps(result)
            assert isinstance(json_str, str), "Skill outputs must be JSON serializable"

            # Should be able to deserialize
            deserialized = json.loads(json_str)
            assert deserialized == result, (
                "JSON round-trip must preserve skill output structure"
            )
