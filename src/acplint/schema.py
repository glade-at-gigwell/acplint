"""Pydantic models for the Agent Client Protocol (ACP) schema.

These models mirror the ACP v1 schema types for strict validation
of agent responses during conformance testing.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# JSON-RPC envelope
# ---------------------------------------------------------------------------

class JsonRpcRequest(BaseModel):
    """A JSON-RPC 2.0 request."""
    model_config = ConfigDict(populate_by_name=True)
    jsonrpc: str = "2.0"
    id: int | str
    method: str
    params: dict[str, Any] | None = None


class JsonRpcError(BaseModel):
    """A JSON-RPC 2.0 error object."""
    model_config = ConfigDict(populate_by_name=True)
    code: int
    message: str
    data: Any | None = None


class JsonRpcResponse(BaseModel):
    """A JSON-RPC 2.0 response."""
    model_config = ConfigDict(populate_by_name=True)
    jsonrpc: str = "2.0"
    id: int | str | None = None
    result: Any | None = None
    error: JsonRpcError | None = None


class JsonRpcNotification(BaseModel):
    """A JSON-RPC 2.0 notification (no id)."""
    model_config = ConfigDict(populate_by_name=True)
    jsonrpc: str = "2.0"
    method: str
    params: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Protocol version
# ---------------------------------------------------------------------------

class ProtocolVersion(str, Enum):
    V1 = "1"


# ---------------------------------------------------------------------------
# Implementation info
# ---------------------------------------------------------------------------

class Implementation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    version: str
    title: str | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Capabilities
# ---------------------------------------------------------------------------

class ClientCapabilities(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    prompts: dict[str, Any] | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class SessionCloseCapabilities(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class SessionCapabilities(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    close: SessionCloseCapabilities | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class AgentCapabilities(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    load_session: bool | None = Field(None, alias="loadSession")
    session_capabilities: SessionCapabilities | None = Field(None, alias="sessionCapabilities")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

class AuthMethod(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    label: str | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------

class SessionMode(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    name: str
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class SessionModeState(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    current_mode_id: str = Field(alias="currentModeId")
    available_modes: list[SessionMode] = Field(alias="availableModes")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class SessionConfigOption(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    label: str
    option_type: str = Field(alias="type")
    default_value: Any | None = Field(None, alias="defaultValue")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class McpServer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    command: str
    args: list[str] | None = None
    env: dict[str, str] | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Initialize
# ---------------------------------------------------------------------------

class InitializeRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    protocol_version: ProtocolVersion = Field(alias="protocolVersion")
    client_capabilities: ClientCapabilities = Field(default_factory=ClientCapabilities, alias="clientCapabilities")
    client_info: Implementation | None = Field(None, alias="clientInfo")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class InitializeResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    protocol_version: ProtocolVersion = Field(alias="protocolVersion")
    agent_capabilities: AgentCapabilities = Field(default_factory=AgentCapabilities, alias="agentCapabilities")
    auth_methods: list[AuthMethod] = Field(default_factory=list, alias="authMethods")
    agent_info: Implementation | None = Field(None, alias="agentInfo")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Authenticate
# ---------------------------------------------------------------------------

class AuthenticateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    method_id: str = Field(alias="methodId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class AuthenticateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Logout
# ---------------------------------------------------------------------------

class LogoutRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class LogoutResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# New session
# ---------------------------------------------------------------------------

class NewSessionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cwd: str
    mcp_servers: list[McpServer] = Field(default_factory=list, alias="mcpServers")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class NewSessionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    modes: SessionModeState | None = None
    config_options: list[SessionConfigOption] | None = Field(None, alias="configOptions")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Load session
# ---------------------------------------------------------------------------

class LoadSessionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    cwd: str
    mcp_servers: list[McpServer] = Field(default_factory=list, alias="mcpServers")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class LoadSessionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    modes: SessionModeState | None = None
    config_options: list[SessionConfigOption] | None = Field(None, alias="configOptions")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Resume session
# ---------------------------------------------------------------------------

class ResumeSessionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    cwd: str
    mcp_servers: list[McpServer] = Field(default_factory=list, alias="mcpServers")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ResumeSessionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    modes: SessionModeState | None = None
    config_options: list[SessionConfigOption] | None = Field(None, alias="configOptions")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Close session
# ---------------------------------------------------------------------------

class CloseSessionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class CloseSessionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# List sessions
# ---------------------------------------------------------------------------

class SessionInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    work_dirs: list[str] | None = Field(None, alias="workDirs")
    title: str | None = None
    updated_at: str | None = Field(None, alias="updatedAt")
    created_at: str | None = Field(None, alias="createdAt")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ListSessionsRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cwd: str | None = None
    cursor: str | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ListSessionsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sessions: list[SessionInfo] = Field(default_factory=list)
    next_cursor: str | None = Field(None, alias="nextCursor")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Delete session
# ---------------------------------------------------------------------------

class DeleteSessionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class DeleteSessionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

class StopReason(str, Enum):
    END_TURN = "end_turn"
    MAX_OUTPUT_TOKENS = "max_output_tokens"
    MAX_TOKENS = "max_tokens"
    MAX_TURN_REQUESTS = "max_turn_requests"
    TOOL_USE = "tool_use"
    REFUSAL = "refusal"
    CANCELLED = "cancelled"


class PromptCapabilities(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    image: bool | None = None
    audio: bool | None = None
    embedded_context: bool | None = Field(None, alias="embeddedContext")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class PromptRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    content: list[dict[str, Any]] = Field(default_factory=list)
    prompt_capabilities: PromptCapabilities | None = Field(None, alias="promptCapabilities")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class PromptResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stop_reason: StopReason | None = Field(None, alias="stopReason")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Cancel notification
# ---------------------------------------------------------------------------

class CancelNotification(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Content blocks
# ---------------------------------------------------------------------------

class TextContent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    text: str
    annotations: dict[str, Any] | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ImageContent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: str
    mime_type: str = Field(alias="mimeType")
    uri: str | None = None
    annotations: dict[str, Any] | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class AudioContent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: str
    mime_type: str = Field(alias="mimeType")
    annotations: dict[str, Any] | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ResourceLink(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    uri: str
    description: str | None = None
    mime_type: str | None = Field(None, alias="mimeType")
    title: str | None = None
    size: int | None = None
    annotations: dict[str, Any] | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class EmbeddedResource(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    resource: dict[str, Any]
    annotations: dict[str, Any] | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ContentBlock(BaseModel):
    """Discriminated union of content block types."""
    model_config = ConfigDict(populate_by_name=True)
    type: str
    text: str | None = None
    data: str | None = None
    mime_type: str | None = Field(None, alias="mimeType")
    uri: str | None = None
    name: str | None = None
    description: str | None = None
    title: str | None = None
    size: int | None = None
    resource: dict[str, Any] | None = None
    annotations: dict[str, Any] | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Content chunks (streaming)
# ---------------------------------------------------------------------------

class ContentChunk(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    content: ContentBlock
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Tool calls
# ---------------------------------------------------------------------------

class ToolKind(str, Enum):
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"
    MOVE = "move"
    SEARCH = "search"
    EXECUTE = "execute"
    THINK = "think"
    FETCH = "fetch"
    SWITCH_MODE = "switch_mode"
    OTHER = "other"


class ToolCallStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ToolCallLocation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    path: str
    line_range: dict[str, int] | None = Field(None, alias="lineRange")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class Diff(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    path: str
    old_text: str | None = Field(None, alias="oldText")
    new_text: str | None = Field(None, alias="newText")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class Terminal(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    terminal_id: str = Field(alias="terminalId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ToolCallContent(BaseModel):
    """Discriminated union of tool call content types."""
    model_config = ConfigDict(populate_by_name=True)
    type: str
    content: Any | None = None
    path: str | None = None
    old_text: str | None = Field(None, alias="oldText")
    new_text: str | None = Field(None, alias="newText")
    terminal_id: str | None = Field(None, alias="terminalId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ToolCall(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tool_call_id: str = Field(alias="toolCallId")
    title: str
    kind: ToolKind = ToolKind.OTHER
    status: ToolCallStatus = ToolCallStatus.PENDING
    content: list[ToolCallContent] = Field(default_factory=list)
    locations: list[ToolCallLocation] = Field(default_factory=list)
    raw_input: Any | None = Field(None, alias="rawInput")
    raw_output: Any | None = Field(None, alias="rawOutput")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ToolCallUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    kind: ToolKind | None = None
    status: ToolCallStatus | None = None
    title: str | None = None
    content: list[ToolCallContent] | None = None
    locations: list[ToolCallLocation] | None = None
    raw_input: Any | None = Field(None, alias="rawInput")
    raw_output: Any | None = Field(None, alias="rawOutput")


class ToolCallUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tool_call_id: str = Field(alias="toolCallId")
    kind: ToolKind | None = None
    status: ToolCallStatus | None = None
    title: str | None = None
    content: list[ToolCallContent] | None = None
    locations: list[ToolCallLocation] | None = None
    raw_input: Any | None = Field(None, alias="rawInput")
    raw_output: Any | None = Field(None, alias="rawOutput")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Plan
# ---------------------------------------------------------------------------

class PlanEntryPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PlanEntryStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class PlanEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    content: str
    priority: PlanEntryPriority
    status: PlanEntryStatus
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class Plan(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    entries: list[PlanEntry]
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Available commands
# ---------------------------------------------------------------------------

class AvailableCommand(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    description: str | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class AvailableCommandsUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    available_commands: list[AvailableCommand] = Field(alias="availableCommands")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Session updates (agent -> client notifications)
# ---------------------------------------------------------------------------

class CurrentModeUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    current_mode_id: str = Field(alias="currentModeId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ConfigOptionUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    config_options: list[SessionConfigOption] = Field(alias="configOptions")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class SessionInfoUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    title: str | None = None
    updated_at: str | None = Field(None, alias="updatedAt")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class UsageUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    used: int
    size: int
    cost: dict[str, Any] | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class SessionUpdate(BaseModel):
    """Discriminated union of session update types.

    Uses the `session_update` discriminator field (wire: `sessionUpdate`).
    """
    model_config = ConfigDict(populate_by_name=True)
    session_update: str = Field(alias="sessionUpdate")
    content: Any | None = None
    tool_call: ToolCall | None = Field(None, alias="toolCall")
    tool_call_update: ToolCallUpdate | None = Field(None, alias="toolCallUpdate")
    plan: Plan | None = None
    available_commands: list[AvailableCommand] | None = Field(None, alias="availableCommands")
    current_mode_id: str | None = Field(None, alias="currentModeId")
    config_options: list[SessionConfigOption] | None = Field(None, alias="configOptions")
    title: str | None = None
    updated_at: str | None = Field(None, alias="updatedAt")
    used: int | None = None
    size: int | None = None
    cost: dict[str, Any] | None = None
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class SessionNotification(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    update: SessionUpdate
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Agent -> Client requests
# ---------------------------------------------------------------------------

class PermissionOptionKind(str, Enum):
    ALLOW_ONCE = "allow_once"
    ALLOW_ALWAYS = "allow_always"
    REJECT_ONCE = "reject_once"
    REJECT_ALWAYS = "reject_always"


class PermissionOptionChoice(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    option_id: str = Field(alias="optionId")
    name: str
    kind: PermissionOptionKind
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class PermissionPattern(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    pattern: str
    display_name: str | None = Field(None, alias="displayName")


class RequestPermissionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    tool_call: ToolCallUpdate = Field(alias="toolCall")
    options: list[PermissionOptionChoice]
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class RequestPermissionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    outcome: dict[str, Any]
    meta: dict[str, Any] | None = Field(None, alias="_meta")


def select_allow_option(options: list[dict[str, Any]]) -> str | None:
    """Pick the optionId of the first allow-kind permission option (ACP v1).

    ACP v1 options carry an explicit ``kind`` (``allow_once``/``allow_always``
    /``reject_once``/``reject_always``); the spec does not guarantee allow-first
    ordering. Auto-approval that blindly selects ``options[0]`` can therefore
    pick a reject-kind option and produce a false negative. This prefers the
    first option whose ``kind`` is an allow variant, falls back to the first
    option's ``optionId`` when no allow-kind option is present, and returns
    ``None`` when there are no options.
    """
    for opt in options or []:
        if opt.get("kind") in ("allow_always", "allow_once"):
            return opt.get("optionId")
    if options:
        return options[0].get("optionId")
    return None


class ReadTextFileRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    path: str
    line_range: dict[str, int] | None = Field(None, alias="lineRange")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ReadTextFileResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    content: str
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class WriteTextFileRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    path: str
    content: str
    old_text: str | None = Field(None, alias="oldText")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class WriteTextFileResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Terminal
# ---------------------------------------------------------------------------

class CreateTerminalRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    label: str | None = None
    cwd: str | None = None
    output_byte_limit: int | None = Field(None, alias="outputByteLimit")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class CreateTerminalResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    terminal_id: str = Field(alias="terminalId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class TerminalOutputRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    terminal_id: str = Field(alias="terminalId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class TerminalOutputResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: str
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ReleaseTerminalRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    terminal_id: str = Field(alias="terminalId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ReleaseTerminalResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class WaitForTerminalExitRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    terminal_id: str = Field(alias="terminalId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class TerminalExitStatus(str, Enum):
    EXITED = "exited"
    FAILED = "failed"


class WaitForTerminalExitResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    status: TerminalExitStatus
    exit_code: int | None = Field(None, alias="exitCode")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class KillTerminalRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    terminal_id: str = Field(alias="terminalId")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class KillTerminalResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Set session mode
# ---------------------------------------------------------------------------

class SetSessionModeRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    mode_id: str
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class SetSessionModeResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Set session config option
# ---------------------------------------------------------------------------

class SetSessionConfigOptionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    option_id: str = Field(alias="optionId")
    value: Any
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class SetSessionConfigOptionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# Fork session
# ---------------------------------------------------------------------------

class ForkSessionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    cwd: str
    mcp_servers: list[McpServer] = Field(default_factory=list, alias="mcpServers")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


class ForkSessionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_id: str = Field(alias="sessionId")
    modes: SessionModeState | None = None
    config_options: list[SessionConfigOption] | None = Field(None, alias="configOptions")
    meta: dict[str, Any] | None = Field(None, alias="_meta")


# ---------------------------------------------------------------------------
# ACP method name constants
# ---------------------------------------------------------------------------

METHOD_INITIALIZE = "initialize"
METHOD_AUTHENTICATE = "authenticate"
METHOD_LOGOUT = "logout"
METHOD_NEW_SESSION = "session/new"
METHOD_LOAD_SESSION = "session/load"
METHOD_LIST_SESSIONS = "session/list"
METHOD_DELETE_SESSION = "session/delete"
METHOD_FORK_SESSION = "session/fork"
METHOD_RESUME_SESSION = "session/resume"
METHOD_CLOSE_SESSION = "session/close"
METHOD_PROMPT = "session/prompt"
METHOD_SET_SESSION_MODE = "session/set_mode"
METHOD_SET_SESSION_CONFIG_OPTION = "session/set_config_option"
METHOD_CANCEL = "session/cancel"
METHOD_SESSION_UPDATE = "session/update"
METHOD_REQUEST_PERMISSION = "session/request_permission"
METHOD_READ_TEXT_FILE = "fs/read_text_file"
METHOD_WRITE_TEXT_FILE = "fs/write_text_file"
METHOD_CREATE_TERMINAL = "terminal/create"
METHOD_TERMINAL_OUTPUT = "terminal/output"
METHOD_RELEASE_TERMINAL = "terminal/release"
METHOD_WAIT_FOR_TERMINAL_EXIT = "terminal/wait_for_exit"
METHOD_KILL_TERMINAL = "terminal/kill"


# Maps method names to their response Pydantic models
METHOD_RESPONSE_MODELS: dict[str, type[BaseModel]] = {
    METHOD_INITIALIZE: InitializeResponse,
    METHOD_AUTHENTICATE: AuthenticateResponse,
    METHOD_LOGOUT: LogoutResponse,
    METHOD_NEW_SESSION: NewSessionResponse,
    METHOD_LOAD_SESSION: LoadSessionResponse,
    METHOD_LIST_SESSIONS: ListSessionsResponse,
    METHOD_DELETE_SESSION: DeleteSessionResponse,
    METHOD_FORK_SESSION: ForkSessionResponse,
    METHOD_RESUME_SESSION: ResumeSessionResponse,
    METHOD_CLOSE_SESSION: CloseSessionResponse,
    METHOD_PROMPT: PromptResponse,
    METHOD_SET_SESSION_MODE: SetSessionModeResponse,
    METHOD_SET_SESSION_CONFIG_OPTION: SetSessionConfigOptionResponse,
    METHOD_REQUEST_PERMISSION: RequestPermissionResponse,
    METHOD_READ_TEXT_FILE: ReadTextFileResponse,
    METHOD_WRITE_TEXT_FILE: WriteTextFileResponse,
    METHOD_CREATE_TERMINAL: CreateTerminalResponse,
    METHOD_TERMINAL_OUTPUT: TerminalOutputResponse,
    METHOD_RELEASE_TERMINAL: ReleaseTerminalResponse,
    METHOD_WAIT_FOR_TERMINAL_EXIT: WaitForTerminalExitResponse,
    METHOD_KILL_TERMINAL: KillTerminalResponse,
}
