import reflex as rx
from .integration import list_proposals, vote, execute_proposal

def create_h3_heading(text):
    """Create an h3 heading with specific styling."""
    return rx.heading(
        text,
        font_weight="500",
        margin_bottom="0.5rem",
        font_size="1.25rem",
        line_height="1.75rem",
        as_="h3",
    )


def create_h2_heading(text):
    """Create an h2 heading with specific styling."""
    return rx.heading(
        text,
        font_weight="600",
        margin_bottom="1rem",
        font_size="1.5rem",
        line_height="2rem",
        as_="h2",
    )


def create_paragraph(text):
    """Create a paragraph with specific styling."""
    return rx.text(
        text, margin_bottom="1rem", color="#4B5563"
    )


def create_styled_button(
    hover_styles, background_color, text
):
    """Create a styled button with customizable hover effects and background color."""
    return rx.el.button(
        text,
        background_color=background_color,
        font_weight="700",
        _hover=hover_styles,
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="0.25rem",
        color="#ffffff",
    )


def create_voting_buttons():
    """Create a flex container with 'Yes' and 'No' voting buttons."""
    return rx.flex(
        create_styled_button(
            hover_styles={"background-color": "#059669"},
            background_color="#10B981",
            text=" Vote Yes ",
        ),
        create_styled_button(
            hover_styles={"background-color": "#DC2626"},
            background_color="#EF4444",
            text=" Vote No ",
        ),
        display="flex",
        column_gap="1rem",
    )


def create_proposal_box(title, description):
    """Create a box containing a proposal title, description, and voting buttons."""
    return rx.box(
        create_h3_heading(text=title),
        create_paragraph(text=description),
        create_voting_buttons(),
        border_bottom_width="1px",
        padding_bottom="1rem",
    )


def create_progress_bar(width):
    """Create a progress bar with a specified width."""
    return rx.box(
        width=width,
        background_color="#3B82F6",
        height="1rem",
        border_radius="9999px",
    )


def create_progress_bar_container(progress_width):
    """Create a container for a progress bar with a specified progress width."""
    return rx.box(
        create_progress_bar(width=progress_width),
        background_color="#E5E7EB",
        height="1rem",
        margin_bottom="0.5rem",
        border_radius="9999px",
    )


def create_text_span(text):
    """Create a text span element."""
    return rx.text.span(text)


def create_result_labels(left_label, right_label):
    """Create a flex container with two labels for voting results."""
    return rx.flex(
        create_text_span(text=left_label),
        create_text_span(text=right_label),
        display="flex",
        justify_content="space-between",
        color="#4B5563",
        font_size="0.875rem",
        line_height="1.25rem",
    )


def create_result_box(
    title, progress_width, yes_percentage, no_percentage
):
    """Create a box displaying voting results with a title, progress bar, and percentages."""
    return rx.box(
        create_h3_heading(text=title),
        create_progress_bar_container(
            progress_width=progress_width
        ),
        create_result_labels(
            left_label=yes_percentage,
            right_label=no_percentage,
        ),
    )


def create_connect_wallet_button():
    """Create a 'Connect Wallet' button with specific styling."""
    return rx.el.button(
        " Connect Wallet ",
        id="connect-wallet",
        background_color="#3B82F6",
        font_weight="700",
        _hover={"background-color": "#2563EB"},
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="0.25rem",
        color="#ffffff",
    )


def create_header():
    """Create the header section with title and wallet connection."""
    return rx.flex(
        rx.heading(
            "DAO Voting System",
            font_weight="700",
            font_size="1.5rem",
            line_height="2rem",
            color="#1F2937",
            as_="h1",
        ),
        rx.box(
            create_connect_wallet_button(),
            rx.text.span(
                id="wallet-address",
                display="none",
                color="#4B5563",
            ),
            id="wallet-section",
        ),
        display="flex",
        align_items="center",
        justify_content="space-between",
    )


def create_header_container():
    """Create a container for the header with responsive styling."""
    return rx.box(
        rx.box(
            create_header(),
            width="100%",
            style=rx.breakpoints(
                {
                    "640px": {"max-width": "640px"},
                    "768px": {"max-width": "768px"},
                    "1024px": {"max-width": "1024px"},
                    "1280px": {"max-width": "1280px"},
                    "1536px": {"max-width": "1536px"},
                }
            ),
            margin_left="auto",
            margin_right="auto",
            padding_left="1.5rem",
            padding_right="1.5rem",
            padding_top="1rem",
            padding_bottom="1rem",
        ),
        background_color="#ffffff",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    )


def create_voting_section():
    """Dynamically create boxes for each proposal using integration.py."""
    proposals = list_proposals()
    proposal_boxes = []
    for prop in proposals:
        prop_box = rx.box(
            rx.heading(f"#{prop['id']} - {prop['title']}", as_="h3"),
            rx.text(prop['description']),
            rx.text(f"For votes: {prop['forVotes']}"),
            rx.text(f"Against votes: {prop['againstVotes']}"),
            rx.button("Vote Yes", on_click=lambda: vote(prop['id'], True, "YOUR_ADDRESS_HERE")),
            rx.button("Vote No", on_click=lambda: vote(prop['id'], False, "YOUR_ADDRESS_HERE")),
            rx.cond(
                prop['executed'],
                rx.text("Proposal Executed"),
                rx.button("Execute", on_click=lambda: execute_proposal(prop['id'], "YOUR_ADDRESS_HERE"))
            ),
            border_bottom_width="1px",
            padding_bottom="1rem",
        )
        proposal_boxes.append(prop_box)
    return rx.box(*proposal_boxes)


def create_results_section():
    """Create the results section displaying voting outcomes."""
    return rx.box(
        create_h2_heading(text="Voting Results"),
        rx.box(
            create_result_box(
                title="Proposal 1 Results",
                progress_width="75%",
                yes_percentage="Yes: 75%",
                no_percentage="No: 25%",
            ),
            create_result_box(
                title="Proposal 2 Results",
                progress_width="60%",
                yes_percentage="Yes: 60%",
                no_percentage="No: 40%",
            ),
            display="flex",
            flex_direction="column",
            gap="1.5rem",
        ),
        id="results-section",
        background_color="#ffffff",
        padding="1.5rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    )


def create_main_content():
    """Create the main content area with voting and results sections."""
    return rx.box(
        create_voting_section(),
        create_results_section(),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        flex_grow="1",
        margin_left="auto",
        margin_right="auto",
        padding_left="1.5rem",
        padding_right="1.5rem",
        padding_top="2rem",
        padding_bottom="2rem",
    )


def create_footer():
    """Create the footer section with copyright information."""
    return rx.box(
        rx.box(
            rx.text(
                "© 2024 DAO Voting System. All rights reserved."
            ),
            width="100%",
            style=rx.breakpoints(
                {
                    "640px": {"max-width": "640px"},
                    "768px": {"max-width": "768px"},
                    "1024px": {"max-width": "1024px"},
                    "1280px": {"max-width": "1280px"},
                    "1536px": {"max-width": "1536px"},
                }
            ),
            margin_left="auto",
            margin_right="auto",
            padding_left="1.5rem",
            padding_right="1.5rem",
            text_align="center",
        ),
        class_name="mt-auto",
        background_color="#1F2937",
        padding_top="1rem",
        padding_bottom="1rem",
        color="#ffffff",
    )


def index():
    """Create the complete DAO voting system page structure."""
    return rx.fragment(
        rx.el.link(
            href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
            rel="stylesheet",
        ),
        rx.el.style(
            """
        @font-face {
            font-family: 'LucideIcons';
            src: url(https://unpkg.com/lucide-static@latest/font/Lucide.ttf) format('truetype');
        }
    """
        ),
        rx.box(
            create_header_container(),
            create_main_content(),
            create_footer(),
            background_color="#F3F4F6",
            display="flex",
            flex_direction="column",
            font_family='system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
            min_height="100vh",
        ),
    )


app = rx.App()
app.add_page(index)
