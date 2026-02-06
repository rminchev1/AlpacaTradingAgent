"""
webui/components/decision_panel.py - Enhanced decision summary panel with prominent signals.
Redesigned for pro trader workflow with color-coded BUY/SELL/HOLD indicators.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html


def create_signal_card():
    """Create the prominent trading signal card."""
    return html.Div([
        # Signal display area - will be updated by callback
        html.Div(
            id="signal-display",
            children=[
                html.Div([
                    html.I(className="fas fa-clock fa-2x mb-2"),
                    html.H5("Awaiting Analysis", className="mb-1"),
                    html.P("Start analysis to see trading signal", className="text-muted small mb-0")
                ], className="text-center py-4")
            ],
            className="signal-card-content"
        )
    ], className="signal-card mb-3", id="signal-card-container")


def create_compact_decision_panel():
    """Create a compact decision panel for the trading sidebar."""
    return html.Div([
        # Prominent Signal Card
        create_signal_card(),

        # Quick Agent Summary (brief 2-3 line insights)
        html.Div([
            html.Div(
                id="agent-quick-summary",
                children=[
                    html.Div(
                        "Agent insights will appear here after analysis",
                        className="text-muted small text-center py-2"
                    )
                ]
            )
        ], className="agent-quick-summary-container mb-3"),

        # Compact decision details (scrollable)
        html.Div([
            html.H6([
                html.I(className="fas fa-file-alt me-2"),
                "Decision Details"
            ], className="mb-2 text-muted"),
            html.Div(
                dcc.Markdown(
                    id="decision-summary",
                    children="Run analysis to see the decision summary",
                    className="dash-markdown compact-markdown"
                ),
                className="decision-details-scroll"
            )
        ], className="decision-details-container")
    ], className="compact-decision-panel")


def create_decision_panel():
    """Create the decision summary panel for the web UI (enhanced version)."""
    return dbc.Card(
        dbc.CardBody([
            html.H4("Decision Summary", className="mb-3"),
            html.Hr(),

            # Prominent Signal Card at top
            create_signal_card(),

            # Detailed decision content
            html.Div(
                dcc.Markdown(
                    id="decision-summary",
                    children="Run analysis to see the final decision summary",
                    className="dash-markdown"
                ),
                style={
                    "height": "300px",
                    "overflowY": "auto",
                    "overflowX": "hidden",
                    "border": "1px solid #334155",
                    "borderRadius": "5px",
                    "padding": "15px",
                    "backgroundColor": "#1E293B"
                }
            )
        ]),
        className="mb-4"
    )


def render_signal_display(signal: str, symbol: str, confidence: float = None,
                          risk_level: str = None, position_size: float = None):
    """
    Render the trading signal display card.

    Args:
        signal: Trading signal - "BUY", "SELL", "HOLD", "LONG", "SHORT", "NEUTRAL"
        symbol: Stock/crypto symbol
        confidence: Confidence percentage (0-100)
        risk_level: Risk level string (e.g., "Low", "Medium", "High")
        position_size: Suggested position size in dollars
    """
    # Normalize signal
    signal_upper = signal.upper() if signal else "HOLD"

    # Signal styling
    signal_styles = {
        "BUY": {"color": "success", "icon": "fa-arrow-up", "bg": "rgba(16, 185, 129, 0.1)"},
        "LONG": {"color": "success", "icon": "fa-arrow-up", "bg": "rgba(16, 185, 129, 0.1)"},
        "SELL": {"color": "danger", "icon": "fa-arrow-down", "bg": "rgba(239, 68, 68, 0.1)"},
        "SHORT": {"color": "danger", "icon": "fa-arrow-down", "bg": "rgba(239, 68, 68, 0.1)"},
        "HOLD": {"color": "warning", "icon": "fa-pause", "bg": "rgba(245, 158, 11, 0.1)"},
        "NEUTRAL": {"color": "secondary", "icon": "fa-minus", "bg": "rgba(148, 163, 184, 0.1)"},
    }

    style = signal_styles.get(signal_upper, signal_styles["HOLD"])

    # Build confidence bar if provided
    confidence_bar = None
    if confidence is not None:
        confidence_color = "success" if confidence >= 70 else ("warning" if confidence >= 50 else "danger")
        confidence_bar = html.Div([
            html.Small("Confidence", className="text-muted"),
            dbc.Progress(
                value=confidence,
                color=confidence_color,
                className="mt-1",
                style={"height": "6px"}
            ),
            html.Small(f"{confidence:.0f}%", className=f"text-{confidence_color} fw-bold")
        ], className="mt-2")

    # Build meta info row
    meta_items = []
    if risk_level:
        risk_colors = {"low": "success", "medium": "warning", "high": "danger"}
        risk_color = risk_colors.get(risk_level.lower(), "secondary")
        meta_items.append(
            html.Span([
                html.I(className="fas fa-shield-alt me-1"),
                f"Risk: ",
                html.Span(risk_level, className=f"text-{risk_color} fw-bold")
            ], className="me-3")
        )
    if position_size:
        meta_items.append(
            html.Span([
                html.I(className="fas fa-dollar-sign me-1"),
                f"Size: ${position_size:,.0f}"
            ])
        )

    meta_row = html.Div(meta_items, className="text-muted small mt-2") if meta_items else None

    return html.Div([
        # Main signal display
        html.Div([
            html.Div([
                html.I(className=f"fas {style['icon']} fa-2x text-{style['color']}"),
            ], className="signal-icon-wrapper"),
            html.Div([
                html.H2(signal_upper, className=f"text-{style['color']} mb-0 fw-bold signal-text"),
                html.H5(symbol.upper(), className="text-white mb-0")
            ], className="signal-text-wrapper")
        ], className="d-flex align-items-center justify-content-center gap-3",
           style={"backgroundColor": style["bg"], "borderRadius": "8px", "padding": "20px"}),

        # Confidence bar
        confidence_bar,

        # Meta info
        meta_row
    ], className="signal-display-content")
