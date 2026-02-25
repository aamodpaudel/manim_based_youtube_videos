from manim import *

from copy_try import SUCCESS_COLOR

# --- Absolute Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Light Pink (The new color for your text)
ACCENT_COLOR = "#be185d"       # Deep Pink
UI_GREY = "#94a3b8"            # Slate for borders
TEXT_DARK = "#1f2937"          # Professional Dark Grey
GRID_COLOR = "#e5e7eb"         # UI Separators

class GoogleSearchCloudComputing(Scene):
    def construct(self):
        # 1. SET GLOBAL BACKGROUND TO WHITE
        self.camera.background_color = WHITE

        # --- 2. THE BROWSER SHELL ---
        browser_canvas = RoundedRectangle(
            height=6.5, width=11, corner_radius=0.15,
            color=PRIMARY_COLOR, stroke_width=2,
            fill_color=WHITE, fill_opacity=1
        )
        
        # Header/Address Bar Area
        header_divider = Line(
            start=browser_canvas.get_corner(UL) + DOWN * 0.8,
            end=browser_canvas.get_corner(UR) + DOWN * 0.8,
            color=GRID_COLOR, stroke_width=1.5
        )

        # Mac-style Window Controls
        window_dots = VGroup(*[
            Dot(radius=0.07, color=c) for c in [ACCENT_COLOR, PRIMARY_COLOR, SECONDARY_COLOR]
        ]).arrange(RIGHT, buff=0.15).move_to(browser_canvas.get_corner(UL) + DR * 0.4)

        # Subtle Address Bar Capsule
        address_bar = RoundedRectangle(
            height=0.4, width=6.5, corner_radius=0.2,
            color=GRID_COLOR, stroke_width=1, fill_color="#f8fafc", fill_opacity=1
        ).move_to(browser_canvas.get_top() + DOWN * 0.4)

        url_label = Text("google.com", font="sans-serif", font_size=14, color=UI_GREY).move_to(address_bar)

        # --- 3. THE LANDING PAGE CONTENT ---
        # Google Logo: Pink, Not Bold
        google_logo = Text("Google", font="serif", font_size=82, color=PRIMARY_COLOR, weight=NORMAL)
        google_logo.shift(UP * 1.1)

        # Search Container
        search_box = RoundedRectangle(
            height=0.8, width=7, corner_radius=0.4,
            color=PRIMARY_COLOR, stroke_width=2, # Highlighted border
            fill_color=WHITE, fill_opacity=1
        ).next_to(google_logo, DOWN, buff=0.7)

        # Search Icon
        search_icon = VGroup(
            Circle(radius=0.1, color=PRIMARY_COLOR, stroke_width=2),
            Line(ORIGIN, DR * 0.08, color=PRIMARY_COLOR, stroke_width=2).shift(DR * 0.07)
        ).next_to(search_box.get_left(), RIGHT, buff=0.3)

        # SEARCH QUERY: Now Light Pink and Vertically Centered
        search_query = Text("Mount Everest", font="sans-serif", font_size=20, color=PRIMARY_COLOR)
        
        # Fix: Precise alignment to the icon and center-y of the box
        search_query.next_to(search_icon, RIGHT, buff=0.3)
        search_query.match_y(search_box)
        
        # Professional Blinking Cursor
        cursor = Line(
            UP * 0.25, DOWN * 0.25, 
            color=PRIMARY_COLOR, stroke_width=2.5
        )
        cursor.next_to(search_icon, RIGHT, buff=0.3)
        cursor.match_y(search_box)

        # UI Buttons
        btn_config = {"height": 0.55, "width": 1.9, "corner_radius": 0.1, "fill_opacity": 1}
        search_btn = RoundedRectangle(color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, **btn_config)
        lucky_btn = RoundedRectangle(color=SECONDARY_COLOR, fill_color=SECONDARY_COLOR, **btn_config)
        
        s_text = Text("Google Search", font_size=12, color=WHITE).move_to(search_btn)
        l_text = Text("I'm Feeling Lucky", font_size=12, color=PRIMARY_COLOR).move_to(lucky_btn)
        
        footer_btns = VGroup(
            VGroup(search_btn, s_text),
            VGroup(lucky_btn, l_text)
        ).arrange(RIGHT, buff=0.5).next_to(search_box, DOWN, buff=0.6)

        # --- ANIMATION SEQUENCE ---

        # 1. Reveal Browser & Branding
        self.play(
            Create(browser_canvas),
            Create(header_divider),
            FadeIn(window_dots),
            Write(url_label),
            Write(google_logo),
            run_time=1.5
        )
        
        # 2. Reveal Search Bar
        self.play(
            Create(search_box),
            FadeIn(search_icon),
            FadeIn(footer_btns, shift=UP*0.2),
            FadeIn(cursor)
        )
        self.wait(0.3)

        # 3. TYPING ANIMATION
        # Cursor follows the light pink text
        cursor.add_updater(lambda m: m.next_to(search_query, RIGHT, buff=0.08))

        self.play(
            AddTextLetterByLetter(search_query),
            run_time=2.5,
            rate_func=linear
        )
        
        self.wait(0.2)
        cursor.remove_updater(cursor.updaters[0])

        # 4. Final Click Interaction
        self.play(
            search_btn.animate.scale(0.95),
            rate_func=there_and_back,
            run_time=0.2
        )
        
        self.play(Blink(cursor, run_time=2))
        self.wait(2)

from manim import *
import numpy as np

# --- Visual Styling ---
PRIMARY_COLOR = "#db2777"
SECONDARY_COLOR = "#fce7f3"
ACCENT_COLOR = "#be185d"
TEXT_DARK = "#1f2937"
TITLE_BLACK = "#000000"

class FastAIInitiative3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = WHITE
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # 1. FIXED UI OVER
        # LAY
        title = Text("The First-Principles AI Gap", color=TITLE_BLACK, font_size=32, weight=NORMAL)
        self.add_fixed_in_frame_mobjects(title)
        title.to_corner(UL, buff=0.5)

        # 2. OPTIMIZED NEURAL NETWORK (Using Dots instead of Spheres)
        def create_layer(nodes_count, z_offset, color):
            layer = VGroup()
            for i in range(nodes_count):
                angle = TAU * i / nodes_count
                pos = [np.cos(angle) * 1.5, np.sin(angle) * 1.5, z_offset]
                # Dot is much lighter than Sphere for rendering
                node = Dot(point=pos, radius=0.1, color=color)
                layer.add(node)
            return layer

        input_layer = create_layer(6, -2, "#94a3b8")
        hidden_layer = create_layer(8, 0, PRIMARY_COLOR)
        output_layer = create_layer(4, 2, PRIMARY_COLOR)

        # Simplified connections (only connecting to some nodes to save render time)
        connections = VGroup()
        for l1, l2 in [(input_layer, hidden_layer), (hidden_layer, output_layer)]:
            for i, n1 in enumerate(l1):
                for j, n2 in enumerate(l2):
                    if (i + j) % 2 == 0: # Only draw 50% of lines for speed/clarity
                        line = Line(n1.get_center(), n2.get_center(), color=SECONDARY_COLOR, stroke_width=1)
                        connections.add(line)

        neural_net = VGroup(input_layer, hidden_layer, output_layer, connections)

        # ACT 1: Intro
        self.play(FadeIn(neural_net), run_time=1)
        self.begin_ambient_camera_rotation(rate=0.1)
        
        info_text = Text("Isolated Model: Zero Context", font_size=18, color=TEXT_DARK)
        self.add_fixed_in_frame_mobjects(info_text)
        info_text.next_to(title, DOWN, buff=0.2).align_to(title, LEFT)
        self.play(Write(info_text))
        self.wait(1)

        # ACT 2: Optimized Vector Cloud (Reduced count for speed)
        vector_cloud = VGroup()
        for _ in range(80): # 80 points is the "sweet spot" for speed vs visual
            p = [np.random.uniform(-3.5, 3.5) for _ in range(3)]
            dot = Dot(point=p, radius=0.03, color=SECONDARY_COLOR, fill_opacity=0.5)
            vector_cloud.add(dot)

        success_text = Text("Solution: Semantic Vector Cloud", font_size=18, color=PRIMARY_COLOR)
        self.add_fixed_in_frame_mobjects(success_text)
        success_text.next_to(title, DOWN, buff=0.2).align_to(title, LEFT)

        self.play(
            FadeOut(info_text),
            Write(success_text),
            FadeIn(vector_cloud),
            neural_net.animate.set_opacity(1),
            run_time=1.5
        )

        # ACT 3: Success Interaction
        hits = VGroup(*[vector_cloud[i] for i in range(10)])
        self.play(hits.animate.set_color(PRIMARY_COLOR).scale(2), run_time=0.5)

        # Final Stat
        summary = Text("Semantic search provides the 'Fuel' for AI.", font_size=18, color=TEXT_DARK)
        self.add_fixed_in_frame_mobjects(summary)
        summary.to_edge(DOWN, buff=0.5)
        self.play(Write(summary))

        self.wait(2)
        self.stop_ambient_camera_rotation()


from manim import *

# Define the custom color palette
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink
ACCENT_COLOR = "#be185d"       # Darker shade
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light grey

class KeywordSearchCheckmark(Scene):
    def construct(self):
        # Set background to white
        self.camera.background_color = WHITE

        # 1. Title (BLACK and NOT bold)
        title = Text("Keyword Search = Exact Word Match", color=BLACK, weight=NORMAL)
        title.scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.add(Underline(title, color=GRID_COLOR))

        # 2. Query UI Setup
        query_label = Text("Query:", color=TEXT_COLOR, font_size=24).to_edge(LEFT, buff=1.5).shift(UP * 1.8)
        query_box = RoundedRectangle(corner_radius=0.1, height=0.7, width=4.5, color=GRID_COLOR, fill_opacity=0.05)
        query_box.next_to(query_label, RIGHT, buff=0.3)
        
        # Initial Query: Everest
        query_text = Text("Everest", color=PRIMARY_COLOR, font_size=28)
        query_text.move_to(query_box.get_center())

        self.play(FadeIn(query_label), Create(query_box), Write(query_text))

        # 3. MCQ Options Setup
        options_raw = [
            "A. Mount Everest is the highest mountain.",
            "B. Everest lies in the Himalayas.",
            "C. The tallest mountain on Earth.",
            "D. K2 is the second-highest mountain after Everest.",
            "E. Kilimanjaro is in Africa."
        ]
        
        options_vgroup = VGroup(*[
            Text(opt, color=TEXT_COLOR, font_size=22) for opt in options_raw
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 0.5)

        self.play(LaggedStart(*[FadeIn(opt) for opt in options_vgroup], lag_ratio=0.1))
        self.wait(1)

        # 4. Phase 1: Search for "Everest"
        # Create pink highlighted text
        match_a = MarkupText(f'A. Mount <span foreground="{PRIMARY_COLOR}">Everest</span> is the highest mountain.', font_size=22, color=TEXT_COLOR)
        match_b = MarkupText(f'B. <span foreground="{PRIMARY_COLOR}">Everest</span> lies in the Himalayas.', font_size=22, color=TEXT_COLOR)
        match_d = MarkupText(f'D. K2 is the second-highest mountain after <span foreground="{PRIMARY_COLOR}">Everest</span>.', font_size=22, color=TEXT_COLOR)
        
        match_a.move_to(options_vgroup[0], aligned_edge=LEFT)
        match_b.move_to(options_vgroup[1], aligned_edge=LEFT)
        match_d.move_to(options_vgroup[3], aligned_edge=LEFT)

        # Create Tickmarks
        tick_a = Text("✔", color=PRIMARY_COLOR, font_size=24).next_to(options_vgroup[0], LEFT, buff=0.4)
        tick_b = Text("✔", color=PRIMARY_COLOR, font_size=24).next_to(options_vgroup[1], LEFT, buff=0.4)
        tick_d = Text("✔", color=PRIMARY_COLOR, font_size=24).next_to(options_vgroup[3], LEFT, buff=0.4)

        result_text_1 = Text("Result: A, B, D", color=PRIMARY_COLOR, font_size=26).next_to(options_vgroup, DOWN, buff=0.8)

        self.play(
            Transform(options_vgroup[0], match_a),
            Transform(options_vgroup[1], match_b),
            Transform(options_vgroup[3], match_d),
            FadeIn(tick_a), FadeIn(tick_b), FadeIn(tick_d),
            Write(result_text_1)
        )
        self.wait(2)

        # 5. Phase 2: Transition to "Mount Everest"
        new_query_text = Text("Mount Everest", color=PRIMARY_COLOR, font_size=28)
        new_query_text.move_to(query_box.get_center())

        # Logic: Options B and D no longer match the exact string "Mount Everest"
        reset_b = Text(options_raw[1], color=TEXT_COLOR, font_size=22).move_to(options_vgroup[1], aligned_edge=LEFT)
        reset_d = Text(options_raw[3], color=TEXT_COLOR, font_size=22).move_to(options_vgroup[3], aligned_edge=LEFT)
        
        # New highlight for A (The full phrase)
        match_a_full = MarkupText(f'A. <span foreground="{PRIMARY_COLOR}">Mount Everest</span> is the highest mountain.', font_size=22, color=TEXT_COLOR)
        match_a_full.move_to(options_vgroup[0], aligned_edge=LEFT)
        
        result_text_2 = Text("Result: A", color=PRIMARY_COLOR, font_size=26).next_to(options_vgroup, DOWN, buff=0.8)

        self.play(
            Transform(query_text, new_query_text),
            FadeOut(result_text_1),
            FadeOut(tick_b), FadeOut(tick_d),
            Transform(options_vgroup[1], reset_b),
            Transform(options_vgroup[3], reset_d),
            Transform(options_vgroup[0], match_a_full)
        )
        self.play(Write(result_text_2))
        
        # Why? Explanation
        explanation = Text("Only option A contains the exact words 'Mount Everest'.", color=TEXT_COLOR, font_size=18)
        explanation.next_to(result_text_2, DOWN, buff=0.3)
        self.play(FadeIn(explanation))

        self.wait(3)
    

from manim import *

# Palette as per instructions
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink
ACCENT_COLOR = "#be185d"       # Darker shade
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light grey

class SemanticSearchScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # 1. Title
        title = Text("Semantic Search = Intent & Context", color=BLACK, weight=NORMAL)
        title.scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.add(Underline(title, color=GRID_COLOR))

        # 2. Query Setup
        query_label = Text("Query:", color=TEXT_COLOR, font_size=24).to_edge(LEFT, buff=1.5).shift(UP * 1.8)
        query_box = RoundedRectangle(corner_radius=0.1, height=0.7, width=4.5, color=PRIMARY_COLOR, fill_opacity=0.05)
        query_box.next_to(query_label, RIGHT, buff=0.3)
        
        query_text = Text("Mount Everest", color=PRIMARY_COLOR, font_size=28)
        query_text.move_to(query_box.get_center())

        self.play(FadeIn(query_label), Create(query_box), Write(query_text))

        # 3. MCQ Options
        options_raw = [
            "A. Mount Everest is the highest mountain.",
            "B. Everest lies in the Himalayas.",
            "C. The tallest mountain on Earth.",
            "D. K2 is the second-highest mountain after Everest.",
            "E. Kilimanjaro is in Africa."
        ]
        
        options_vgroup = VGroup(*[
            Text(opt, color=TEXT_COLOR, font_size=22) for opt in options_raw
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 0.5)

        self.play(LaggedStart(*[FadeIn(opt) for opt in options_vgroup], lag_ratio=0.1))
        self.wait(1)

        # 4. Semantic Highlighting
        # Highlight A (Exact), B (Synonym), C (Description)
        match_a = MarkupText(f'<span foreground="{PRIMARY_COLOR}">A. Mount Everest</span> is the highest mountain.', font_size=22, color=TEXT_COLOR)
        match_b = MarkupText(f'<span foreground="{PRIMARY_COLOR}">B. Everest</span> lies in the Himalayas.', font_size=22, color=TEXT_COLOR)
        match_c = MarkupText(f'<span foreground="{PRIMARY_COLOR}">C. The tallest mountain on Earth.</span>', font_size=22, color=TEXT_COLOR)
        
        match_a.move_to(options_vgroup[0], aligned_edge=LEFT)
        match_b.move_to(options_vgroup[1], aligned_edge=LEFT)
        match_c.move_to(options_vgroup[2], aligned_edge=LEFT)

        # Tickmarks for semantic matches
        ticks = VGroup(*[
            Text("✔", color=PRIMARY_COLOR, font_size=24).next_to(options_vgroup[i], LEFT, buff=0.4)
            for i in range(3)
        ])

        result_text = Text("Result: A, B, C", color=PRIMARY_COLOR, font_size=26).next_to(options_vgroup, DOWN, buff=0.8)

        # 5. Animation Logic: Meaning Mapping
        # We simulate the AI "thinking" or mapping concepts
        self.play(
            Transform(options_vgroup[0], match_a),
            Transform(options_vgroup[1], match_b),
            Transform(options_vgroup[2], match_c),
            FadeIn(ticks),
            Write(result_text)
        )
        self.wait(1)

        # Explanation
        explanation = Text("Why? They all refer to the same concept/intent.", color=TEXT_COLOR, font_size=18)
        explanation.next_to(result_text, DOWN, buff=0.3)
        self.play(FadeIn(explanation))

        self.wait(3)

from manim import *

# Define the custom color palette as per requirements
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink
ACCENT_COLOR = "#be185d"       # Darker shade
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light grey

class CloudQueryIntro(Scene):
    def construct(self):
        # Set background to white
        self.camera.background_color = WHITE

        # 1. Title: "Our focus text" (BLACK, NOT bold)
        title = Text("Our focus text", color=BLACK, weight=NORMAL, font_size=36)
        title.to_edge(UP, buff=0.6)

        # 2. Alphabet Grid (2 rows, 13 columns)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        row1_text = alphabet[:13]
        row2_text = alphabet[13:]

        row1 = VGroup(*[Text(char, color=TEXT_COLOR, font_size=30) for char in row1_text])
        row2 = VGroup(*[Text(char, color=TEXT_COLOR, font_size=30) for char in row2_text])
        
        row1.arrange(RIGHT, buff=0.5)
        row2.arrange(RIGHT, buff=0.5)
        
        alphabet_grid = VGroup(row1, row2).arrange(DOWN, buff=0.6)
        # Position alphabet below title with a clear gap
        alphabet_grid.next_to(title, DOWN, buff=1.0)

        # 3. Search Interface Setup (Fixed at the bottom)
        search_label = Text("Search Topic:", color=TEXT_COLOR, font_size=20)
        search_box = RoundedRectangle(
            corner_radius=0.1, 
            height=0.8, 
            width=6, 
            color=GRID_COLOR, 
            fill_opacity=0.1
        )
        
        # Position UI at the bottom
        search_ui = VGroup(search_label, search_box).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        search_ui.to_edge(DOWN, buff=1.2)

        # 4. Animation Sequence
        self.play(Write(title))
        self.play(
            LaggedStart(*[FadeIn(l) for l in alphabet_grid.submobjects], lag_ratio=0.02),
            run_time=1.5
        )
        self.play(Create(search_box), Write(search_label))
        self.wait(0.5)

        # 5. Typing Animation: "Cloud Computing"
        target_text = "Reduce Cloud Costs"
        typed_mob = Text("", color=PRIMARY_COLOR, font_size=26).move_to(search_box.get_center())
        
        current_str = ""
        for char in target_text:
            current_str += char
            new_typed = Text(current_str, color=PRIMARY_COLOR, font_size=32).move_to(search_box.get_center())
            # Fast transformation to simulate typing
            self.play(Transform(typed_mob, new_typed), run_time=0.08)
            self.wait(0.04)
        
        self.wait(0.5)

        # 6. Highlight Logic
        # Identify unique letters in the query to find in the grid
        query_chars = set(target_text.upper().replace(" ", ""))
        highlight_boxes = VGroup()

        for char in query_chars:
            # Iterate through the grid to find the matching letter mobject
            for row in alphabet_grid:
                for letter_mob in row:
                    if letter_mob.text == char:
                        box = SurroundingRectangle(
                            letter_mob, 
                            color=PRIMARY_COLOR, 
                            buff=0.15,
                            stroke_width=2
                        )
                        highlight_boxes.add(box)

        # Final Reveal: All highlights appear at once after typing
        self.play(
            LaggedStart(*[Create(b) for b in highlight_boxes], lag_ratio=0.05),
            run_time=1.2
        )
        
        self.wait(3)


from manim import *

# Define custom color palette
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink
ACCENT_COLOR = "#be185d"       # Darker shade
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light grey

class AIUnderstandingScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- 1. Title (BLACK, NOT bold, top edge) ---
        title = Text("Semantic Search: Understanding Intent", color=BLACK, weight=NORMAL, font_size=32)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title, run_time=2))

        # --- 2. Word Data Definitions ---
        # 3 Single Words | 3 Two-word phrases | 3 Long phrases (4-5 words)
        # Positioned within a safe Y-range [-1.5 to 1.5] to avoid footer
        words_data = [
            # Related Cluster (Focus: Infrastructure & Setup)
            {"text": "Server", "pos": [-2, 1, 0], "related": True},
            {"text": "Compute", "pos": [0, 1.5, 0], "related": True},
            {"text": "Cloud Hosting", "pos": [1.8, 1, 0], "related": True},
            {"text": "Provision a virtual machine", "pos": [-2.2, -0.8, 0], "related": True},
            {"text": "Reduce Cloud Costs", "pos": [0, -1.5, 0], "related": True},
            {"text": "Auto-scaling web server cluster", "pos": [2.2, -0.8, 0], "related": True},
            
            # Outliers (Cloud themed but different domains)
            {"text": "Storage", "pos": [-4.5, 0.5, 0], "related": False},
            {"text": "Network Security", "pos": [4.5, 0.5, 0], "related": False},
            
        ]

        dots = VGroup()
        labels = VGroup()
        related_dots = []

        # Logic to place labels: Move them OUTWARDS from the center (0,0,0) 
        # to ensure lines connecting dots in the middle don't cross the text.
        for data in words_data:
            dot = Dot(point=data["pos"], color=GRID_COLOR, radius=0.1)
            label = Text(data["text"], color=TEXT_COLOR, font_size=18)
            
            # Calculate direction from center to push label away
            pos_vec = np.array(data["pos"])
            direction = pos_vec / np.linalg.norm(pos_vec) if np.linalg.norm(pos_vec) > 0 else DOWN
            
            label.next_to(dot, direction, buff=0.35)
            
            dots.add(dot)
            labels.add(label)
            if data["related"]:
                related_dots.append(dot)

        # --- 3. Connections (Initial Gray) ---
        # Connect the cluster in a sequence to show a semantic web
        gray_lines = VGroup()
        for i in range(len(related_dots)):
            line = Line(
                related_dots[i].get_center(), 
                related_dots[(i + 1) % len(related_dots)].get_center(), 
                color=GRID_COLOR, 
                stroke_width=2
            )
            gray_lines.add(line)

        # --- 4. Animation Sequence (Slow and Deliberate) ---
        # Reveal Dots and Words
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.2),
            LaggedStart(*[Write(l) for l in labels], lag_ratio=0.2),
            run_time=4
        )
        self.wait(1)

        # Draw gray lines
        self.play(Create(gray_lines), run_time=3)
        self.wait(1.5)

        # --- 5. Semantic Understanding (Highlight Pink) ---
        # Transition lines and dots to Primary Pink
        self.play(
            gray_lines.animate.set_color(PRIMARY_COLOR).set_stroke(width=4),
            *[d.animate.set_color(PRIMARY_COLOR).scale(1.4) for d in related_dots],
            run_time=3
        )
        self.wait(1)

        # --- 6. Conclusion (Strictly Bottom Positioned) ---
        conclusion = Text("AI focuses on intents, not just keywords.", 
                          color=PRIMARY_COLOR, weight=NORMAL, font_size=26)
        
        # Position with a large buffer from the bottom to ensure no overlap with graph
        conclusion.to_edge(DOWN, buff=1.0)
        
        # Adding a light background box to ensure text stands out
        bg_box = SurroundingRectangle(
            conclusion, 
            color=SECONDARY_COLOR, 
            fill_color=SECONDARY_COLOR, 
            fill_opacity=0.9, 
            buff=0.2
        )
        
        self.play(
            FadeIn(bg_box), 
            Write(conclusion, run_time=2.5)
        )
        self.wait(4)

from manim import *
import numpy as np

# Define custom color palette as per instructions
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink
ACCENT_COLOR = "#be185d"       # Darker shade
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light grey

class VectorEmbeddingScene(Scene):
    def construct(self):
        # Set background to white for clarity
        self.camera.background_color = WHITE

        # --- 1. TITLE SECTION ---
        # Requirement: BLACK and NOT bold
        title = Text("How Semantic Search Works", color=BLACK, font_size=32, weight=NORMAL)
        title.to_edge(UP, buff=0.7)

        # --- 2. INPUT DATA BLOCK (Text Only) ---
        input_box = RoundedRectangle(corner_radius=0.1, width=3.8, height=2.2, color=TEXT_COLOR)
        input_label = Text("Information Source", color=TEXT_COLOR, font_size=18).next_to(input_box, UP, buff=0.2)
        
        # Focus purely on text queries as requested
        text_data_1 = Text('Textual Input', color=TEXT_COLOR, font_size=16)
        text_data_2 = Text('"Reduce Cloud Costs"', color=TEXT_COLOR, font_size=16)
        
        inputs_vgroup = VGroup(text_data_1, text_data_2).arrange(DOWN, buff=0.4)
        inputs_vgroup.move_to(input_box.get_center())
        
        input_section = VGroup(input_box, input_label, inputs_vgroup).to_edge(LEFT, buff=0.6)

        # --- 3. THE EMBEDDING MODEL (Center) ---
        model_box = Rectangle(width=2.8, height=3.2, color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=0.1)
        model_label = Text("Vector\nEmbedding\nModel", color=PRIMARY_COLOR, font_size=20, weight=NORMAL)
        model_label.move_to(model_box.get_center())
        
        model_section = VGroup(model_box, model_label)

        # --- 4. THE NUMERICAL VECTOR (Right) ---
        # Represents the mathematical coordinates of the text
        vector_math = MathTex(
            r"\begin{bmatrix} 0.12 \\ -0.85 \\ 0.43 \\ \vdots \\ 0.91 \end{bmatrix}",
            color=TEXT_COLOR
        ).scale(0.8)
        
        vector_box = RoundedRectangle(corner_radius=0.1, width=2.2, height=3.5, color=PRIMARY_COLOR)
        vector_label = Text("Vector", color=PRIMARY_COLOR, font_size=18).next_to(vector_box, UP, buff=0.2)
        
        vector_section = VGroup(vector_box, vector_label, vector_math).to_edge(RIGHT, buff=0.6)

        # Connectors
        arrow1 = Arrow(input_box.get_right(), model_box.get_left(), color=GRID_COLOR, buff=0.1)
        arrow2 = Arrow(model_box.get_right(), vector_box.get_left(), color=PRIMARY_COLOR, buff=0.1)

        # --- 5. CENTERED RELATIONSHIP WEB ---
        # Coordinate system to show semantic proximity
        coord_grid = NumberPlane(
            x_range=[-5, 5, 1], 
            y_range=[-3, 3, 1], 
            background_line_style={"stroke_opacity": 0.3, "stroke_color": GRID_COLOR}
        ).center()

        node_style = {"color": PRIMARY_COLOR, "radius": 0.12}
        
        # High Similarity Nodes
        node_cost = Dot(point=[-1.5, 0.5, 0], **node_style)
        label_cost = Text("Reduce Cloud Costs", font_size=18, color=TEXT_COLOR).next_to(node_cost, UP, buff=0.15)
        
        node_spending = Dot(point=[-1.0, -0.8, 0], **node_style)
        label_spending = Text("Minimize Spending", font_size=18, color=TEXT_COLOR).next_to(node_spending, DOWN, buff=0.15)
        
        # Dissimilar Node
        node_cloud = Dot(point=[2.5, 1.2, 0], color=GRID_COLOR, radius=0.12)
        label_cloud = Text("Rain Cloud", font_size=18, color=TEXT_COLOR).next_to(node_cloud, RIGHT, buff=0.15)

        # Similarity Indicator
        rel_line = Line(node_cost.get_center(), node_spending.get_center(), color=PRIMARY_COLOR, stroke_width=4)
        rel_label = Text("High Similarity", font_size=14, color=PRIMARY_COLOR).next_to(rel_line, LEFT, buff=0.2)

        # --- ANIMATION SEQUENCE ---

        # Phase 1: Conversion Process
        self.play(Write(title))
        self.play(
            Create(input_section),
            Create(model_section),
            GrowArrow(arrow1),
            run_time=2
        )
        self.play(
            GrowArrow(arrow2),
            FadeIn(vector_section, shift=LEFT),
            run_time=1.5
        )
        self.wait(2)

        # Transition to conceptual space
        self.play(
            FadeOut(input_section), 
            FadeOut(model_section), 
            FadeOut(arrow1), 
            FadeOut(arrow2),
            FadeOut(vector_section),
            run_time=1.5
        )

        # Phase 2: The Semantic Map
        self.play(Create(coord_grid), run_time=1.5)
        self.play(
            Create(node_cost), Write(label_cost),
            Create(node_spending), Write(label_spending),
            Create(node_cloud), Write(label_cloud),
            run_time=2
        )
        self.wait(0.5)
        self.play(Create(rel_line), Write(rel_label))
        
        # Final descriptive conclusion (Positioned to avoid overlap)
        conclusion = Text("Focusing on the intent, not prioritizing words.", 
                          color=PRIMARY_COLOR, font_size=24).to_edge(DOWN, buff=0.6)
        
        # Decorative box for conclusion
        bg_rect = SurroundingRectangle(conclusion, color=SECONDARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=1, buff=0.2)
        
        self.play(FadeIn(bg_rect), Write(conclusion))
        self.wait(3)

from manim import *
import numpy as np

# --- Configuration & Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Light Pink Accents
ACCENT_COLOR = "#be185d"       # Darker shade for math
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light Grey

class SemanticMathAnimations(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # ==========================================================
        # SCENE 1: Semantic Understanding (Cosine Similarity)
        # ==========================================================
        title_1 = Text("Semantic Understanding: Cosine Similarity", color=BLACK, font_size=32, weight=NORMAL)
        title_1.to_edge(UP, buff=0.5)

        # Sentences with Pink Vector Labels (Using Arrow head symbols)
        label_a_pink = MathTex(r"\vec{A}:", color=PRIMARY_COLOR, font_size=24)
        text_a = Text('"We need to reduce cloud costs."', color=TEXT_COLOR, font_size=18)
        sentence_a = VGroup(label_a_pink, text_a).arrange(RIGHT, buff=0.2)

        label_b_pink = MathTex(r"\vec{B}:", color=PRIMARY_COLOR, font_size=24)
        text_b = Text('"We should optimize our infrastructure spending."', color=TEXT_COLOR, font_size=18)
        sentence_b = VGroup(label_b_pink, text_b).arrange(RIGHT, buff=0.2)

        sentences = VGroup(sentence_a, sentence_b).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        sentences.to_edge(LEFT, buff=0.8).shift(UP * 1.5)

        # Vector Graph Logic
        plane = NumberPlane(
            x_range=[-0.5, 4, 1], y_range=[-0.5, 4, 1],
            background_line_style={"stroke_color": GRID_COLOR, "stroke_opacity": 0.5}
        ).scale(0.8).shift(DOWN * 0.5 + RIGHT * 1.5)
        
        origin = plane.coords_to_point(0, 0)
        coord_a = np.array([3.0, 0.8, 0])
        coord_b = np.array([2.2, 2.2, 0])
        
        vec_a = Arrow(origin, plane.coords_to_point(*coord_a), buff=0, color=PRIMARY_COLOR, stroke_width=6)
        vec_b = Arrow(origin, plane.coords_to_point(*coord_b), buff=0, color=ACCENT_COLOR, stroke_width=6)

        # Vector Labels in Graph
        graph_label_a = MathTex(r"\vec{A}", color=PRIMARY_COLOR, font_size=24).next_to(vec_a.get_end(), RIGHT, buff=0.2)
        graph_label_b = MathTex(r"\vec{B}", color=ACCENT_COLOR, font_size=24).next_to(vec_b.get_end(), UP, buff=0.2)
        
        # Theta Logic (Ensuring it does NOT touch lines)
        angle_a = np.arctan2(coord_a[1], coord_a[0])
        angle_b = np.arctan2(coord_b[1], coord_b[0])
        theta_arc = Arc(radius=0.7, start_angle=angle_a, angle=angle_b-angle_a, arc_center=origin, color=TEXT_COLOR)
        # Position label further out so it doesn't touch the arc or the vectors
        theta_label = MathTex(r"\theta", color=TEXT_COLOR, font_size=28).move_to(
            theta_arc.point_from_proportion(0.5)
        ).shift(RIGHT * 0.4 + UP * 0.1)
        
        # Explanation Text
        cosine_val = MathTex(r"\cos(\theta) = 0.94", color=PRIMARY_COLOR).next_to(sentences, DOWN, buff=1, aligned_edge=LEFT)
        explanation = Text(
            "θ low means same direction so same\nintent and higher cosine value", 
            font_size=16, color=TEXT_COLOR, line_spacing=0.8
        ).next_to(cosine_val, DOWN, aligned_edge=LEFT, buff=0.4)

        # Animation Sequence 1
        self.play(Write(title_1))
        self.play(FadeIn(sentences, shift=RIGHT))
        self.play(Create(plane), GrowArrow(vec_a), GrowArrow(vec_b))
        self.play(Write(graph_label_a), Write(graph_label_b))
        self.play(Create(theta_arc), Write(theta_label))
        self.play(Write(cosine_val), Write(explanation))
        self.wait(3)

        # Transition
        self.play(FadeOut(Group(*self.mobjects)))

        # ==========================================================
        # SCENE 2: Mathematical Calculation (Dot Product)
        # ==========================================================
        title_2 = Text("Mathematical Calculation: Dot Product", color=BLACK, font_size=32, weight=NORMAL)
        title_2.to_edge(UP, buff=0.5)

        # Vector Components
        vec_a_math = MathTex(r"\vec{v}_A = [0.80, \ 0.50]", color=PRIMARY_COLOR).scale(0.9)
        vec_b_math = MathTex(r"\vec{v}_B = [0.75, \ 0.48]", color=TEXT_COLOR).scale(0.9)
        vec_block = VGroup(vec_a_math, vec_b_math).arrange(RIGHT, buff=1.5).shift(UP * 1.5)

        # Calculation Workflow
        formula = MathTex(r"\vec{v}_A \cdot \vec{v}_B = (a_1 \times b_1) + (a_2 \times b_2)", color=TEXT_COLOR).scale(0.8)
        calc_step_1 = MathTex(r"= (0.80 \times 0.87) + (0.50 \times 0.48)", color=TEXT_COLOR).scale(0.8)
        calc_step_2 = MathTex(r"= 0.696 + 0.24", color=TEXT_COLOR).scale(0.8)
        
        # Final Score with Outline Box (Specific Placement)
        final_score = MathTex(r"\text{Similarity Score} = 0.936", color=PRIMARY_COLOR).scale(1.2)
        score_box = SurroundingRectangle(final_score, color=PRIMARY_COLOR, buff=0.3)
        result_group = VGroup(final_score, score_box)

        # Layout Stack
        math_stack = VGroup(vec_block, formula, calc_step_1, calc_step_2, result_group).arrange(DOWN, buff=0.6)
        math_stack.move_to(ORIGIN).shift(DOWN * 0.2)

        # Animation Sequence 2
        self.play(Write(title_2))
        self.play(FadeIn(vec_block, shift=UP))
        self.play(Write(formula))
        self.play(Write(calc_step_1))
        self.play(Write(calc_step_2))
        self.wait(0.5)
        # Emphasize the final result being the only part boxed
        self.play(Write(final_score))
        self.play(Create(score_box))
        self.wait(4)


from manim import *

# --- Configuration & Palette ---
PRIMARY_COLOR = "#db2777"     # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"   # Light Pink
ACCENT_COLOR = "#be185d"      # Darker Pink
TEXT_COLOR = BLACK            # High contrast text
TITLE_COLOR = BLACK           # Titles: Black and not bold
GRID_COLOR = "#e5e7eb"        # Light gray
UNMATCHED_COLOR = "#94a3b8"   # Gray for lower similarity

class NumericalSimilarityMapping(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- SECTION 1: THE NUMERICAL TABLE ---
        table_title = Text("Query: Mount Everest", color=TITLE_COLOR, weight=NORMAL).scale(0.8)
        table_title.to_edge(UP, buff=0.5)

        table_data = [
            ["Mount Washington", "0.89"],
            ["Nepal", "0.72"],
            ["Pacific Ocean", "0.31"],
            ["Tokyo", "0.14"],
            ["São Paulo", "0.11"]
        ]

        sim_table = Table(
            table_data,
            col_labels=[
                Text("Option", color=TEXT_COLOR), 
                Text("Similarity Score", color=TEXT_COLOR)
            ],
            include_outer_lines=True,
            line_config={"color": GRID_COLOR, "stroke_width": 2}
        ).scale(0.5).next_to(table_title, DOWN, buff=0.7)

        # Apply Colors
        sim_table.get_entries((2, 1)).set_color(PRIMARY_COLOR)
        sim_table.get_entries((2, 2)).set_color(PRIMARY_COLOR)
        
        for i in range(3, 7):
            sim_table.get_entries((i, 1)).set_color(UNMATCHED_COLOR)
            sim_table.get_entries((i, 2)).set_color(UNMATCHED_COLOR)

        # Animation: Row-by-Row Reveal
        self.play(Write(table_title))
        self.play(Create(sim_table.get_horizontal_lines()), Create(sim_table.get_vertical_lines()))
        self.play(Write(sim_table.get_labels()))
        
        rows = sim_table.get_rows()
        for i in range(1, len(rows)):
            self.play(FadeIn(rows[i], shift=UP * 0.2), run_time=0.6)
            self.wait(0.2)

        self.wait(2)
        self.play(FadeOut(sim_table), FadeOut(table_title))

        # --- SECTION 2: THE SEMANTIC SPATIAL GRAPH ---
        graph_title = Text("Semantic Vector Proximity", color=TITLE_COLOR, weight=NORMAL).scale(0.8)
        graph_title.to_edge(UP, buff=0.5)

        everest_dot = Dot(point=ORIGIN, color=PRIMARY_COLOR, radius=0.15)
        everest_label = Text("Mount Everest", color=PRIMARY_COLOR, font_size=24).next_to(everest_dot, UP, buff=0.4)

        # Optimized points_config to prevent overlap
        # São Paulo moved to Top Right (UR quadrant)
        points_config = [
            {"label": "Mount Washington", "pos": RIGHT*2.0 + DOWN*0.5, "dir": DR, "color": PRIMARY_COLOR, "high": True},
            {"label": "Nepal", "pos": LEFT*2.5 + UP*1.5, "dir": UL, "color": UNMATCHED_COLOR, "high": False},
            {"label": "Pacific Ocean", "pos": RIGHT*1.5 + DOWN*2.5, "dir": DL, "color": UNMATCHED_COLOR, "high": False},
            {"label": "Tokyo", "pos": LEFT*4.0 + DOWN*1.5, "dir": DL, "color": UNMATCHED_COLOR, "high": False},
            {"label": "São Paulo", "pos": RIGHT*4.0 + UP*2.5, "dir": UR, "color": UNMATCHED_COLOR, "high": False},
        ]

        self.play(Write(graph_title))
        self.play(Create(everest_dot), Write(everest_label))

        for pt in points_config:
            target_dot = Dot(point=pt["pos"], color=pt["color"], radius=0.1)
            label = Text(pt["label"], color=pt["color"], font_size=20).next_to(target_dot, pt["dir"], buff=0.3)
            
            line = Line(
                everest_dot.get_center(), 
                target_dot.get_center(), 
                color=pt["color"], 
                stroke_width=2 if not pt["high"] else 4, 
                buff=0.15
            ).set_opacity(0.3 if not pt["high"] else 1)
            
            if pt["high"]:
                check = Text("✅", font_size=20, color=PRIMARY_COLOR).next_to(label, RIGHT, buff=0.1)
                self.play(
                    Create(line), 
                    FadeIn(target_dot), 
                    Write(label), 
                    FadeIn(check), 
                    run_time=1
                )
            else:
                self.play(
                    Create(line), 
                    FadeIn(target_dot), 
                    Write(label), 
                    run_time=0.5
                )

        footer = Text("Spatial distance illustrates mathematical cosine similarity.", 
                      color=UNMATCHED_COLOR, font_size=16).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(footer))
        self.wait(3)

from manim import *

# --- Configuration & Palette ---
PRIMARY_COLOR = "#db2777"     # Pinkish-Red (Theme)
SECONDARY_COLOR = WHITE       # Background
TEXT_COLOR = BLACK            # Main text
TITLE_COLOR = BLACK           # Titles (Black & Not Bold)
GRID_COLOR = "#e5e7eb"        # Light gray structure
UNMATCHED_COLOR = "#94a3b8"   # Gray for lower scores

class SemanticTextSimilarity(Scene):
    def construct(self):
        # Force White Background
        self.camera.background_color = WHITE

        # --- QUERY SECTION ---
        # Rule 1c: Title is BLACK and NOT bold
        query_label = Text("Input Query:", color=TITLE_COLOR, font_size=24, weight=NORMAL).to_edge(UP, buff=0.4)
        
        # Query text scaled to roughly 0.75x of previous massive version
        query_text = Text(
            '"I dream of climbing mount Everest once in my lifetime. \n I would like to learn mountain climbing."',
            color=PRIMARY_COLOR,
            font_size=24, # Adjusted for 0.75x feel
            line_spacing=1.2
        ).next_to(query_label, DOWN, buff=0.3)

        # --- DATA PREPARATION ---
        table_content = [
            ["Mountaineering is a very challenging professional career but can be very satisfying.", "0.72"],
            ["We teach people how to climb mountain, provide all the gears and training", "0.94"],
            ["Mountains, peaks and valleys make Switzerland the wonderland of the world.", "0.45"],
            ["Artists love creating pictures - they often imagine natural sceneries and landscapes...", "0.31"],
            ["Lets go hiking today, we have a lot of mountains in New Hampshire to pick from.", "0.58"]
        ]

        # Generating Mobjects for the grid
        mobjects_grid = []
        for i, row in enumerate(table_content):
            # Column 1: The Sentence
            # Using font_size 32 (0.75x of the 42 used previously)
            sentence = Paragraph(
                row[0], 
                color=TEXT_COLOR, 
                font_size=32, 
                line_spacing=0.8, 
                alignment="left"
            )
            sentence.set_width(8.5) # Slightly narrower for better framing
            
            # Column 2: The Score
            score_color = PRIMARY_COLOR if i == 1 else UNMATCHED_COLOR
            score = Text(row[1], color=score_color, font_size=36)
            
            mobjects_grid.append([sentence, score])

        # Headers
        header_1 = Text("Semantic Match Options", color=TITLE_COLOR, font_size=28, weight=NORMAL)
        header_2 = Text("Score", color=TITLE_COLOR, font_size=28, weight=NORMAL)

        # Initialize Table
        # No .scale() here to maintain the precise 0.75x font sizes defined above
        sim_table = MobjectTable(
            mobjects_grid,
            col_labels=[header_1, header_2],
            include_outer_lines=True,
            line_config={"color": GRID_COLOR, "stroke_width": 2},
            h_buff=0.7, 
            v_buff=0.3
        )
        
        # Position the table professionally
        sim_table.next_to(query_text, DOWN, buff=0.5)

        # --- ANIMATION LOGIC ---
        self.play(FadeIn(query_label, shift=UP*0.2))
        self.play(Write(query_text))
        self.wait(0.5)

        # Show Grid Structure
        self.play(
            Create(sim_table.get_horizontal_lines()), 
            Create(sim_table.get_vertical_lines()),
            FadeIn(sim_table.get_labels())
        )
        self.wait(0.5)

        # Reveal Rows sequentially
        rows = sim_table.get_rows()
        for i in range(1, len(rows)):
            self.play(
                FadeIn(rows[i], shift=RIGHT * 0.4),
                run_time=0.6
            )
            
            # Subtle highlight for the winning match
            if i == 2: 
                self.play(rows[i].animate.set_background_stroke(color=PRIMARY_COLOR, opacity=0.1, width=2))
            
            self.wait(0.15)

        # Footer
        footer = Text("Similarity is calculated via Cosine Similarity between vector embeddings.", 
                      color=UNMATCHED_COLOR, font_size=16).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(footer))
        
        self.wait(4)

from manim import *

# --- Configuration & Palette ---
PRIMARY_COLOR = "#db2777"     # Pinkish-Red (Theme/Highlight)
SECONDARY_COLOR = WHITE       # Background
TEXT_COLOR = BLACK            # Main text
TITLE_COLOR = BLACK           # Titles (Black & Not Bold)
GRID_COLOR = "#e5e7eb"        # Light gray structure
UNMATCHED_COLOR = "#94a3b8"   # Gray for lower scores

class SemanticSimilarityRephrased(Scene):
    def construct(self):
        # Force White Background
        self.camera.background_color = WHITE

        # --- QUERY SECTION ---
        # Rule 1c: Title is BLACK and NOT bold
        query_label = Text("Input Query (Rephrased):", color=TITLE_COLOR, font_size=24, weight=NORMAL).to_edge(UP, buff=0.4)
        
        # The new, rephrased query text
        query_text = Text(
            '"I want to learn mountain climbing because my dream is to climb Mount Everest one day"',
            color=PRIMARY_COLOR,
            font_size=24, # Maintaining the 0.75x scale feel
            line_spacing=1.2
        ).next_to(query_label, DOWN, buff=0.3)

        # --- DATA PREPARATION ---
        # Updated scores based on the new query semantic proximity
        table_content = [
            ["Mountaineering is a very challenging professional career but can be very satisfying.", "0.70"],
            ["We teach people how to climb mountain, provide all the gears and training", "0.96"], # Still the best match
            ["Mountains, peaks and valleys make Switzerland the wonderland of the world.", "0.42"],
            ["Artists love creating pictures - they often imagine natural sceneries and landscapes...", "0.28"],
            ["Lets go hiking today, we have a lot of mountains in New Hampshire to pick from.", "0.55"]
        ]

        # Generating Mobjects for the grid with consistent styling
        mobjects_grid = []
        for i, row in enumerate(table_content):
            # Column 1: The Sentence
            sentence = Paragraph(
                row[0], 
                color=TEXT_COLOR, 
                font_size=32, 
                line_spacing=0.8, 
                alignment="left"
            )
            sentence.set_width(8.5)
            
            # Column 2: The Score
            # Row 1 (index 1) is the high match
            score_color = PRIMARY_COLOR if i == 1 else UNMATCHED_COLOR
            score = Text(row[1], color=score_color, font_size=36)
            
            mobjects_grid.append([sentence, score])

        # Headers
        header_1 = Text("Semantic Match Options", color=TITLE_COLOR, font_size=28, weight=NORMAL)
        header_2 = Text("Score", color=TITLE_COLOR, font_size=28, weight=NORMAL)

        # Initialize Table
        sim_table = MobjectTable(
            mobjects_grid,
            col_labels=[header_1, header_2],
            include_outer_lines=True,
            line_config={"color": GRID_COLOR, "stroke_width": 2},
            h_buff=0.7, 
            v_buff=0.3
        )
        
        # Position the table professionally below the new query
        sim_table.next_to(query_text, DOWN, buff=0.6)

        # --- ANIMATION LOGIC ---
        self.play(FadeIn(query_label, shift=UP*0.2))
        self.play(Write(query_text), run_time=1.5)
        self.wait(0.5)

        # Show Grid Structure
        self.play(
            Create(sim_table.get_horizontal_lines()), 
            Create(sim_table.get_vertical_lines()),
            FadeIn(sim_table.get_labels())
        )
        self.wait(0.5)

        # Reveal Rows sequentially
        rows = sim_table.get_rows()
        for i in range(1, len(rows)):
            self.play(
                FadeIn(rows[i], shift=RIGHT * 0.4),
                run_time=0.6
            )
            
            # Subtle highlight for the winning match (Index 2 covers header + row 1)
            if i == 2: 
                self.play(rows[i].animate.set_background_stroke(color=PRIMARY_COLOR, opacity=0.1, width=2))
            
            self.wait(0.15)

        # Footer
        footer = Text("Even with rephrased input, the semantic intent remains the same, yielding similar high scores.", 
                      color=UNMATCHED_COLOR, font_size=14).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(footer))
        
        self.wait(4)

from manim import *

# --- Configuration & Palette ---
PRIMARY_COLOR = "#db2777"     # Pinkish-Red
SECONDARY_COLOR = WHITE       # Background
TEXT_COLOR = BLACK            # Main text
TITLE_COLOR = BLACK           # Titles (Black & Not Bold)
GRID_COLOR = "#e5e7eb"        # Light gray structure
UNMATCHED_COLOR = "#94a3b8"   # Gray for lower scores

class MultiIntentSimilarity(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- DATA DEFINITIONS ---
        options_text = [
            "Mountaineering is a very challenging professional career but can be very satisfying.",
            "We teach people how to climb mountain, provide all the gears and training",
            "Mountains, peaks and valleys make Switzerland the wonderland of the world.",
            "Artists love creating pictures - they often imagine natural sceneries and landscapes...",
            "Lets go hiking today, we have a lot of mountains in New Hampshire to pick from."
        ]

        # Phase 1: Landscape/Viewing Intent
        query_1 = "I dream of seeing Mount Everest once in my lifetime. I love beautiful mountain landscapes."
        scores_1 = ["0.65", "0.58", "0.89", "0.92", "0.71"] # Higher for visual/landscape options

        # Phase 2: Learning/Skill Intent
        query_2 = "I want to learn mountain climbing and outdoor survival skills."
        scores_2 = ["0.82", "0.95", "0.40", "0.35", "0.62"] # Higher for technical/training options

        # --- PHASE 1 ANIMATION ---
        self.run_similarity_phase(query_1, scores_1, "Intent: Aesthetic Appreciation", winner_idx=3)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # --- PHASE 2 ANIMATION ---
        self.run_similarity_phase(query_2, scores_2, "Intent: Technical Skill", winner_idx=1)
        self.wait(3)

    def run_similarity_phase(self, query_str, scores, phase_label_str, winner_idx):
        # 1. Title & Query
        phase_label = Text(phase_label_str, color=UNMATCHED_COLOR, font_size=18).to_edge(UP, buff=0.2)
        query_label = Text("Input Query:", color=TITLE_COLOR, font_size=24, weight=NORMAL).next_to(phase_label, DOWN, buff=0.2)
        
        query_text = Text(
            f'"{query_str}"',
            color=PRIMARY_COLOR,
            font_size=24,
            line_spacing=1.2,
            t2w={query_str: NORMAL}
        ).next_to(query_label, DOWN, buff=0.3)

        self.play(FadeIn(phase_label), Write(query_label))
        self.play(Write(query_text))

        # 2. Build Table Data
        mobjects_grid = []
        for i in range(len(scores)):
            sentence = Paragraph(
                ["Mountaineering is a career...", 
                 "We teach climbing...", 
                 "Switzerland wonderland...", 
                 "Artists/sceneries...", 
                 "Hiking in NH..."][i], # Shortened for code clarity, logic uses full list below
                color=TEXT_COLOR, font_size=32, line_spacing=0.8, alignment="left"
            )
            # Use actual full text from outer scope
            full_text = [
                "Mountaineering is a very challenging professional career but can be very satisfying.",
                "We teach people how to climb mountain, provide all the gears and training",
                "Mountains, peaks and valleys make Switzerland the wonderland of the world.",
                "Artists love creating pictures - they often imagine natural sceneries and landscapes...",
                "Lets go hiking today, we have a lot of mountains in New Hampshire to pick from."
            ]
            sentence = Paragraph(full_text[i], color=TEXT_COLOR, font_size=32, line_spacing=0.8).set_width(8.5)
            
            score_color = PRIMARY_COLOR if i == winner_idx else UNMATCHED_COLOR
            score = Text(scores[i], color=score_color, font_size=36)
            mobjects_grid.append([sentence, score])

        header_1 = Text("Semantic Match Options", color=TITLE_COLOR, font_size=28, weight=NORMAL)
        header_2 = Text("Score", color=TITLE_COLOR, font_size=28, weight=NORMAL)

        sim_table = MobjectTable(
            mobjects_grid,
            col_labels=[header_1, header_2],
            include_outer_lines=True,
            line_config={"color": GRID_COLOR, "stroke_width": 2},
            h_buff=0.7, v_buff=0.3
        ).next_to(query_text, DOWN, buff=0.5)

        # 3. Animate Table
        self.play(Create(sim_table.get_horizontal_lines()), Create(sim_table.get_vertical_lines()), FadeIn(sim_table.get_labels()))
        
        rows = sim_table.get_rows()
        for i in range(1, len(rows)):
            self.play(FadeIn(rows[i], shift=RIGHT * 0.4), run_time=0.5)
            if i == winner_idx + 1: # +1 because row 0 is header
                self.play(rows[i].animate.set_background_stroke(color=PRIMARY_COLOR, opacity=0.15, width=3), run_time=0.3)
            self.wait(0.1)


from manim import *

# --- Configuration & Palette ---
PRIMARY_COLOR = "#db2777"     # Pinkish-Red (High Similarity)
SECONDARY_COLOR = WHITE       # Background
TEXT_COLOR = BLACK            # Main text
TITLE_COLOR = BLACK           # Titles (Black & Not Bold)
GRID_COLOR = "#e5e7eb"        # Light gray for table structure
UNMATCHED_COLOR = "#94a3b8"   # Gray for lower scores

class SemanticAgentRouting(Scene):
    def construct(self):
        # Rule 1b: Force White Background
        self.camera.background_color = WHITE

        # --- QUERY SECTION ---
        # Rule 1c: Title is BLACK and NOT bold
        query_label = Text("Production Input Query:", color=TITLE_COLOR, font_size=32, weight=NORMAL).to_edge(UP, buff=0.3)
        
        query_text = Text(
            '"Why did our cloud bill spike last month and how can we reduce it?"',
            color=PRIMARY_COLOR,
            font_size=30, 
            line_spacing=1.2
        ).next_to(query_label, DOWN, buff=0.2)

        # --- AGENT DATA ---
        agents_data = [
            ["Agent 1 – Finance Assistant: Budgeting, forecasting, and expense categorization.", "0.78"],
            ["Agent 2 – Cloud Cost Optimization: Analyzes usage metrics, spend, and resources.", "0.96"],
            ["Agent 3 – HR Assistant: Answers questions on payroll, hiring, and benefits.", "0.12"],
            ["Agent 4 – DevOps Troubleshooting: Monitors failures, logs, and performance.", "0.65"],
            ["Agent 5 – Sales Analytics: Analyzes pipeline performance and revenue trends.", "0.15"]
        ]

        # Preparing the grid with significantly larger internal font sizes
        mobjects_grid = []
        for i, row in enumerate(agents_data):
            # Column 1: The Agent Description
            # font_size 38 provides high legibility
            desc = Paragraph(
                row[0], 
                color=TEXT_COLOR, 
                font_size=38, 
                line_spacing=0.8, 
                alignment="left"
            )
            # set_width is increased to 11 to fill the widescreen frame
            desc.set_width(11) 
            
            # Column 2: The Score
            score_color = PRIMARY_COLOR if i == 1 else UNMATCHED_COLOR
            score = Text(row[1], color=score_color, font_size=42)
            
            mobjects_grid.append([desc, score])

        # Headers - Balanced with table size
        header_1 = Text("Available AI Agents", color=TITLE_COLOR, font_size=36, weight=NORMAL)
        header_2 = Text("Score", color=TITLE_COLOR, font_size=36, weight=NORMAL)

        # Initialize MobjectTable
        # Scale increased to 0.85 to make the table clearly visible across the screen
        sim_table = MobjectTable(
            mobjects_grid,
            col_labels=[header_1, header_2],
            include_outer_lines=True,
            line_config={"color": GRID_COLOR, "stroke_width": 2.5},
            h_buff=0.8, 
            v_buff=0.4
        ).scale(0.85).next_to(query_text, DOWN, buff=0.5)

        # --- ANIMATION LOGIC ---
        self.play(FadeIn(query_label, shift=UP*0.2))
        self.play(Write(query_text))
        self.wait(0.5)

        # Show Grid Structure
        # Rule 2b: Ensure no text overlaps with lines by using Create
        self.play(
            Create(sim_table.get_horizontal_lines()), 
            Create(sim_table.get_vertical_lines()),
            FadeIn(sim_table.get_labels())
        )

        # Reveal Rows Sequentially
        rows = sim_table.get_rows()
        for i in range(1, len(rows)):
            self.play(
                FadeIn(rows[i], shift=RIGHT * 0.4),
                run_time=0.6
            )
            
            # Highlight Agent 2 as the winning selection
            if i == 2: 
                self.play(
                    rows[i].animate.set_background_stroke(color=PRIMARY_COLOR, opacity=0.15, width=5),
                    run_time=0.3
                )
                self.play(Indicate(rows[i][1], color=PRIMARY_COLOR))
            
            self.wait(0.1)

        # Result Footer - High contrast
        footer = Text("System selects Agent 2 based on highest Semantic Proximity", 
                      color=PRIMARY_COLOR, font_size=24).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(footer))
        
        self.wait(4)

from manim import *

# --- Configuration & Palette ---
PRIMARY_COLOR = "#db2777"     # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"   # Very Light Pink (Accents)
TEXT_COLOR = BLACK            # High contrast text for white background
TITLE_COLOR = BLACK           # Titles: black and not bold
GRID_COLOR = "#e5e7eb"        # Light grey for borders
UNMATCHED_COLOR = "#94a3b8"   # Gray for lower similarity

class ReasoningWorkflowFixed(Scene):
    def construct(self):
        # Set Background to WHITE as requested
        self.camera.background_color = WHITE

        # --- 1. THE QUERY SECTION ---
        # Rule 1c: Title is BLACK and NOT bold
        query_label = Text("User Input Query:", color=TITLE_COLOR, font_size=24, weight=NORMAL).to_edge(UP, buff=0.4)
        
        query_text = Text(
            '"I need advanced equipment for a high-altitude technical climb."',
            color=PRIMARY_COLOR, font_size=32
        ).next_to(query_label, DOWN, buff=0.2)

        # --- 2. THE OPTION BOXES (LARGE SENTENCES, SMALLER SCORES) ---
        
        # Option A
        opt1_desc = Paragraph(
            "Option A: We provide specialized technical gear for high-altitude expeditions and mountaineering.", 
            color=TEXT_COLOR, font_size=108, width=6, alignment="left"
        )
        # Similarity Score decreased in size as requested
        opt1_score = Text("Similarity Score: 0.95", color=PRIMARY_COLOR, font_size=20).next_to(opt1_desc, DOWN, buff=0.3)
        
        opt1_content = VGroup(opt1_desc, opt1_score).center()
        
        opt1_rect = RoundedRectangle(
            corner_radius=0.2, 
            height=opt1_content.height + 1.2, 
            width=opt1_content.width + 1, 
            color=PRIMARY_COLOR, 
            stroke_width=4
        ).move_to(opt1_content)
        
        opt1_box = VGroup(opt1_rect, opt1_content).scale(0.75).to_edge(LEFT, buff=0.5).shift(UP*0.3)

        # Option B
        opt2_desc = Paragraph(
            "Option B: Our shop offers advanced climbing equipment and expert advice for technical ascents.", 
            color=TEXT_COLOR, font_size=108, width=6, alignment="left"
        )
        opt2_score = Text("Similarity Score: 0.94", color=UNMATCHED_COLOR, font_size=20).next_to(opt2_desc, DOWN, buff=0.3)
        
        opt2_content = VGroup(opt2_desc, opt2_score).center()
        
        opt2_rect = RoundedRectangle(
            corner_radius=0.2, 
            height=opt2_content.height + 1.2, 
            width=opt2_content.width + 1, 
            color=GRID_COLOR, 
            stroke_width=2
        ).move_to(opt2_content)
        
        opt2_box = VGroup(opt2_rect, opt2_content).scale(0.75).to_edge(RIGHT, buff=0.5).shift(UP*0.3)

        # --- 3. THE REASONING BOX ---
        reasoning_label = Text("AI Reasoning Module", color=PRIMARY_COLOR, font_size=24, weight=NORMAL)
        reasoning_desc = Paragraph(
            "Analyzing domain-specific logic to break the similarity tie between Option A and Option B based on technical specifications.",
            color=TEXT_COLOR, font_size=28, width=10, alignment="center"
        ).next_to(reasoning_label, DOWN, buff=0.2)
        
        reasoning_content = VGroup(reasoning_label, reasoning_desc).center()
        
        # Using SECONDARY_COLOR (Light Pink) for the reasoning box fill
        reasoning_rect = RoundedRectangle(
            corner_radius=0.3, 
            height=reasoning_content.height + 1, 
            width=reasoning_content.width + 1, 
            color=PRIMARY_COLOR, 
            fill_color=SECONDARY_COLOR, 
            fill_opacity=1,
            stroke_width=2
        ).to_edge(DOWN, buff=0.7)
        
        reasoning_content.move_to(reasoning_rect.get_center())
        llm_box = VGroup(reasoning_rect, reasoning_content)

        # --- ANIMATION SEQUENCE ---
        self.play(Write(query_label))
        self.play(Write(query_text))
        self.wait(0.5)

        # Show Options - Large sentences are now highly visible
        self.play(
            FadeIn(opt1_box, shift=UP*0.3),
            FadeIn(opt2_box, shift=UP*0.3)
        )
        self.wait(0.5)

        # Final Reasoning Box
        self.play(GrowFromEdge(llm_box, DOWN))
        
        # Visual indication of the reasoning choice
        self.play(
            opt1_rect.animate.set_stroke(width=10),
            opt2_rect.animate.set_stroke(width=1, opacity=0.3),
            opt2_content.animate.set_opacity(0.3)
        )
        
        self.wait(4)

from manim import *

# --- Configuration & Palette ---
PRIMARY_COLOR = "#db2777"     # Pinkish-Red (Theme)
SECONDARY_COLOR = "#fce7f3"   # Light Pink (Fills)
TEXT_COLOR = BLACK            # High contrast
TITLE_COLOR = BLACK           # Not bold
GRID_COLOR = "#e5e7eb"        # Light gray borders

class DatabaseEvolution(Scene):
    def construct(self):
        # Set Background to WHITE
        self.camera.background_color = WHITE

        # ==========================================
        # SCENE 1: THE PAST - FIXED HORIZONTAL ARROW
        # ==========================================
        title_past = Text("The Past: Structured Data & SQL", color=TITLE_COLOR, font_size=32, weight=NORMAL).to_edge(UP, buff=0.5)

        # Structured Table
        table_rect = Rectangle(height=2.5, width=4, color=GRID_COLOR, fill_color=WHITE, fill_opacity=1)
        rows = VGroup(*[Line(table_rect.get_left() + UP*i, table_rect.get_right() + UP*i, color=GRID_COLOR) for i in [-0.5, 0, 0.5]])
        cols = Line(table_rect.get_top(), table_rect.get_bottom(), color=GRID_COLOR)
        table_label = Text("Structured Data\n(Tables)", color=TEXT_COLOR, font_size=24).next_to(table_rect, DOWN, buff=0.3)
        structured_group = VGroup(table_rect, rows, cols, table_label).to_edge(LEFT, buff=1.2)

        # SQL Database Box
        db_box = RoundedRectangle(corner_radius=0.2, height=2.5, width=4.5, color=PRIMARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=1)
        sql_label = Text("SQL Database", color=TEXT_COLOR, font_size=28).next_to(db_box, UP, buff=0.3)
        sql_code = Text("SELECT * FROM costs;", color=PRIMARY_COLOR, font_size=24, font="Consolas").move_to(db_box)
        sql_group = VGroup(db_box, sql_label, sql_code).to_edge(RIGHT, buff=1.2)

        # FIXED HORIZONTAL ARROW: Aligning Y-coordinates perfectly
        y_center_past = table_rect.get_center()[1] 
        arrow_past = Arrow(
            start=[structured_group.get_right()[0] + 0.1, y_center_past, 0], 
            end=[sql_group.get_left()[0] - 0.1, y_center_past, 0], 
            color=PRIMARY_COLOR, 
            buff=0
        )

        self.play(Write(title_past))
        self.play(FadeIn(structured_group), FadeIn(sql_group), GrowArrow(arrow_past))
        self.wait(2)
        self.play(FadeOut(title_past), FadeOut(structured_group), FadeOut(sql_group), FadeOut(arrow_past))

        # ==========================================
        # SCENE 2: TODAY - FIXED HORIZONTAL ARROW
        # ==========================================
        title_today = Text("Today: Unstructured Data & Vectors", color=TITLE_COLOR, font_size=32, weight=NORMAL).to_edge(UP, buff=0.5)

        # Document Icon
        doc_rect = RoundedRectangle(corner_radius=0.1, height=2.5, width=2, color=GRID_COLOR, fill_color=WHITE, fill_opacity=1)
        doc_lines = VGroup(*[Line(doc_rect.get_left() + RIGHT*0.3 + UP*i, doc_rect.get_right() - RIGHT*0.3 + UP*i, color=GRID_COLOR) for i in [0.6, 0.3, 0, -0.3, -0.6]])
        doc_label = Text("Unstructured\nDocument", color=TEXT_COLOR, font_size=24).next_to(doc_rect, DOWN, buff=0.3)
        doc_group = VGroup(doc_rect, doc_lines, doc_label).to_edge(LEFT, buff=1.5)

        # Vector Representation
        vector_box = RoundedRectangle(corner_radius=0.2, height=1.5, width=5, color=PRIMARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=1)
        vector_text = Text("[0.12, -0.98, 0.45, ...]", color=PRIMARY_COLOR, font_size=28, font="Consolas").move_to(vector_box)
        vector_label = Text("Vector Representation", color=TEXT_COLOR, font_size=24).next_to(vector_box, UP, buff=0.3)
        vector_group = VGroup(vector_box, vector_text, vector_label).to_edge(RIGHT, buff=1.5)

        # FIXED HORIZONTAL ARROW: Aligning Y-coordinates perfectly
        y_center_today = doc_rect.get_center()[1]
        arrow_today = Arrow(
            start=[doc_group.get_right()[0] + 0.1, y_center_today, 0], 
            end=[vector_group.get_left()[0] - 0.1, y_center_today, 0], 
            color=PRIMARY_COLOR, 
            buff=0
        )

        self.play(Write(title_today))
        self.play(FadeIn(doc_group), FadeIn(vector_group), GrowArrow(arrow_today))
        self.wait(2)
        self.play(FadeOut(title_today), FadeOut(doc_group), FadeOut(vector_group), FadeOut(arrow_today))

        # ==========================================
        # SCENE 3: WEAVIATE QUERY & CENTERED SUMMARY
        # ==========================================
        title_weaviate = Text("Weaviate Semantic Query: Cloud Optimization", color=TITLE_COLOR, font_size=32, weight=NORMAL).to_edge(UP, buff=0.4)

        table_data = [
            ["ID", "URL", "Semantic Match Snippet"],
            ["DOC_001", "/aws/cost-tips", "Leverage spot instances for stateless workloads."],
            ["DOC_002", "/finops/guide", "Identify idle resources and automated shutdowns."],
            ["DOC_003", "/cloud/saving", "Use reserved instances for consistent traffic."],
            ["DOC_004", "/azure/spend", "Scale down non-production environments after hours."],
            ["DOC_005", "/gcp/billing", "Analyze multi-cloud egress costs for optimization."]
        ]

        mobjects_grid = []
        for i, row in enumerate(table_data):
            f_size = 28 if i == 0 else 22
            color = PRIMARY_COLOR if i == 0 else TEXT_COLOR
            r1 = Text(row[0], font_size=f_size, color=color, font="Consolas")
            r2 = Text(row[1], font_size=f_size, color=color, font="Consolas")
            r3 = Paragraph(row[2], font_size=f_size, color=color, width=6)
            mobjects_grid.append([r1, r2, r3])

        # Table positioned towards the top
        res_table = MobjectTable(
            mobjects_grid,
            include_outer_lines=True,
            line_config={"color": GRID_COLOR, "stroke_width": 2},
            h_buff=0.8, v_buff=0.4
        ).scale(0.55).next_to(title_weaviate, DOWN, buff=0.4)

        # Summary text positioned in the center, right after the table
        summary_text = Text(
            "Semantic search instantly retrieves the most relevant matches\nfrom millions of unstructured documents based on meaning.",
            color=PRIMARY_COLOR,
            font_size=20,
            line_spacing=1.2,
            weight=NORMAL
        ).next_to(res_table, DOWN, buff=0.6)

        self.play(Write(title_weaviate))
        self.play(Create(res_table.get_horizontal_lines()), Create(res_table.get_vertical_lines()))
        self.play(Write(res_table.get_entries()))
        
        # Highlight top result row
        self.play(res_table.get_rows()[1].animate.set_background_stroke(color=PRIMARY_COLOR, opacity=0.2, width=4))

        # Final Summary Animation centered right after the table
        self.play(FadeIn(summary_text, shift=UP*0.3))
        self.wait(5)

class AwesomeAISuccessScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- 1. HEADER GROUP ---
        # Rule: Title is BLACK and NOT bold
        title = Text("The AI Production Challenge", color=BLACK, font_size=36, weight=NORMAL)
        subtitle = Text("MIT Sloan & BCG Study: Implementation Gap", color=TEXT_COLOR, font_size=18)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.3)

        # --- 2. THE PROPER BAR CHART ---
        chart_width = 9
        
        # Create a background frame for the bar
        bg_bar = RoundedRectangle(
            corner_radius=0.05, 
            width=chart_width, 
            height=0.8, 
            color=GRID_COLOR, 
            fill_opacity=0.3, 
            stroke_width=1
        )
        
        # The 95% Failure Bar
        # We start with a very small width to animate growth correctly
        fail_bar = Rectangle(
            width=0.01, 
            height=0.7, 
            color=PRIMARY_COLOR, 
            fill_opacity=1, 
            stroke_width=0
        )
        fail_bar.align_to(bg_bar, LEFT).shift(RIGHT * 0.05) # Small padding from edge

        # Labels positioned strictly relative to the bar frame to prevent overlap
        label_fail = Text("95% FAIL IN PRODUCTION", color=PRIMARY_COLOR, font_size=20, weight=BOLD)
        label_fail.next_to(bg_bar, UP, buff=0.4).align_to(bg_bar, LEFT)
        
        label_success = Text("5% SUCCESS", color=TEXT_COLOR, font_size=16)
        label_success.next_to(bg_bar, RIGHT, buff=0.5)

        # Grouping chart elements
        chart_group = VGroup(label_fail, bg_bar, fail_bar, label_success)

        # --- 3. THE FOUNDATION BLOCK ---
        foundation_box = RoundedRectangle(
            corner_radius=0.15, 
            height=1.8, 
            width=8, 
            color=PRIMARY_COLOR, 
            stroke_width=2,
            fill_color=SECONDARY_COLOR,
            fill_opacity=0.3
        )
        
        f_title = Text("Foundation: Semantic Search", color=BLACK, font_size=26, weight=NORMAL)
        f_desc = Text(
            "Understanding intent is the prerequisite for AI ROI.", 
            color=TEXT_COLOR, 
            font_size=18
        )
        
        foundation_content = VGroup(f_title, f_desc).arrange(DOWN, buff=0.3)
        foundation_content.move_to(foundation_box.get_center())
        
        foundation_group = VGroup(foundation_box, foundation_content)

        # --- 4. MASTER LAYOUT ENGINE ---
        # Forces a 1.2 unit gap between every major section
        master_layout = VGroup(header, chart_group, foundation_group).arrange(DOWN, buff=1.2)
        master_layout.center()

        # --- ANIMATION SEQUENCE ---
        self.play(FadeIn(header, shift=UP))
        self.wait(0.5)

        # Bar Chart Animation
        self.play(Create(bg_bar), Write(label_success))
        
        # Fixed the rate function reference
        self.play(
            fail_bar.animate.stretch_to_fit_width(chart_width * 0.94).align_to(bg_bar, LEFT).shift(RIGHT*0.05),
            run_time=2,
            rate_func=bezier([0, 0, 1, 1]) # Custom smooth curve
        )
        self.play(Write(label_fail))
        self.wait(1)

        # Foundation Animation
        self.play(
            Create(foundation_box),
            Write(foundation_content),
            run_time=1.2
        )
        
        # Subtle "Pulse" highlight for the foundation
        self.play(foundation_box.animate.set_stroke(width=6), run_time=0.4)
        self.play(foundation_box.animate.set_stroke(width=2), run_time=0.4)

        self.wait(3)

class MeaningMatchScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- 1. TITLE SECTION ---
        title = Text("Keyword Search", color=BLACK, font_size=32, weight=NORMAL)
        title.to_edge(UP, buff=0.7)

        # --- 2. INPUT TEXT BLOCK ---
        input_label = Text("Given Text:", color=TEXT_COLOR, font_size=18)
        # We define the query clearly
        input_query = Text('"Reduce cloud costs"', color=PRIMARY_COLOR, font_size=28, weight=BOLD)
        
        input_group = VGroup(input_label, input_query).arrange(DOWN, buff=0.2)
        input_group.shift(UP * 1.5)

        # --- 3. OPTIONS LIST (Using MarkupText for precise highlighting) ---
        option_font_size = 22

        # Option 1: Wrapping keywords in spans for perfect color isolation
        opt1_text = MarkupText(
            f'1. How to <span foreground="{PRIMARY_COLOR}">reduce</span> <span foreground="{PRIMARY_COLOR}">cloud</span> <span foreground="{PRIMARY_COLOR}">costs</span> in AWS',
            color=TEXT_COLOR, font_size=option_font_size
        )
        
        # Option 2
        opt2_text = MarkupText(
            f'2. Best practices to <span foreground="{PRIMARY_COLOR}">reduce</span> <span foreground="{PRIMARY_COLOR}">cloud</span> <span foreground="{PRIMARY_COLOR}">costs</span>',
            color=TEXT_COLOR, font_size=option_font_size
        )
        
        # Option 3 (No highlights as per keyword logic)
        opt3_text = MarkupText(
            '3. Cloud cost optimization strategies',
            color=TEXT_COLOR, font_size=option_font_size
        )

        options_vgroup = VGroup(opt1_text, opt2_text, opt3_text).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        options_vgroup.shift(DOWN * 0.5)

        # --- 4. VISUAL CUES (GREEN TICKS) ---
        tick1 = Tex(r"\checkmark", color=SUCCESS_COLOR).scale(1.2).next_to(opt1_text, RIGHT, buff=0.5)
        tick2 = Tex(r"\checkmark", color=SUCCESS_COLOR).scale(1.2).next_to(opt2_text, RIGHT, buff=0.5)

        # --- ANIMATION SEQUENCE ---
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(input_group, shift=DOWN))
        self.wait(1)

        # Animation Group for clean entry
        self.play(
            AnimationGroup(
                FadeIn(opt1_text, shift=RIGHT),
                FadeIn(opt2_text, shift=RIGHT),
                FadeIn(opt3_text, shift=RIGHT),
                lag_ratio=0.3
            )
        )
        self.wait(1)

        # Show Green Ticks only for the keyword matches
        self.play(Write(tick1), Write(tick2))
        
        # Final descriptive note
        note = Text("Keyword Search: Matches exact characters only", 
                    color=TEXT_COLOR, font_size=16, slant=ITALIC)
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note))

        self.wait(3)

from manim import *

# Define custom color palette
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light grey

class PreciseRouting(Scene):
    def construct(self):
        # Set background to white
        self.camera.background_color = WHITE

        # --- Title ---
        title = Text("Semantic Intent Routing", color=BLACK, font_size=32, weight=NORMAL)
        title.to_edge(UP, buff=0.5)

        # --- Constructing Components ---
        
        # 1. Input Section
        input_box = RoundedRectangle(corner_radius=0.1, height=1.2, width=2.2, color=GRID_COLOR)
        input_label = Text("User Input", font_size=18, color=TEXT_COLOR)
        input_grp = VGroup(input_box, input_label)

        # 2. Router Section (The 'Brain')
        router_box = RoundedRectangle(corner_radius=0.1, height=1.8, width=3.0, color=PRIMARY_COLOR)
        router_label = Text("Semantic Router", font_size=20, color=TEXT_COLOR)
        router_grp = VGroup(router_box, router_label)

        # 3. Destination Sections
        dest_style = {"corner_radius": 0.1, "height": 1.1, "width": 2.8, "color": GRID_COLOR}
        
        kb_box = RoundedRectangle(**dest_style)
        kb_text = Text("Knowledge Base", font_size=18, color=TEXT_COLOR)
        kb_grp = VGroup(kb_box, kb_text)

        ppl_box = RoundedRectangle(**dest_style)
        ppl_text = Text("People (Experts)", font_size=18, color=TEXT_COLOR)
        ppl_grp = VGroup(ppl_box, ppl_text)

        # AI Agents text split into two lines
        ai_box = RoundedRectangle(**dest_style)
        ai_line1 = Text("AI Agents", font_size=18, color=TEXT_COLOR)
        ai_line2 = Text("(Digital Workers)", font_size=14, color=TEXT_COLOR).next_to(ai_line1, DOWN, buff=0.1)
        ai_grp = VGroup(ai_box, ai_line1, ai_line2)

        destinations = VGroup(kb_grp, ppl_grp, ai_grp).arrange(DOWN, buff=0.6)

        # --- Layout and Centering ---
        # Group everything to center it on the screen
        main_ui = VGroup(input_grp, router_grp, destinations).arrange(RIGHT, buff=1.8)
        main_ui.move_to(ORIGIN) # Perfectly centered
        
        # --- Connections (Defined strictly between box edges) ---
        line_in_to_router = Line(input_box.get_right(), router_box.get_left(), color=GRID_COLOR)
        line_router_to_kb = Line(router_box.get_right(), kb_box.get_left(), color=GRID_COLOR)
        line_router_to_ppl = Line(router_box.get_right(), ppl_box.get_left(), color=GRID_COLOR)
        line_router_to_ai = Line(router_box.get_right(), ai_box.get_left(), color=GRID_COLOR)

        # --- Rendering Elements ---
        self.play(Write(title))
        self.play(
            Create(input_grp), 
            Create(router_grp), 
            Create(destinations),
            Create(line_in_to_router),
            Create(line_router_to_kb),
            Create(line_router_to_ppl),
            Create(line_router_to_ai),
            run_time=2
        )
        self.wait(1)

        # --- Routing Animation Logic ---
        def route_packet(query_string, target_line, target_box):
            # Create text below the input box
            query_label = Text(f"Query: {query_string}", font_size=16, color=TEXT_COLOR)
            query_label.next_to(input_box, DOWN, buff=0.5)
            
            # Create the packet (dot)
            dot = Dot(color=PRIMARY_COLOR, radius=0.1)
            
            # 1. Show query
            self.play(FadeIn(query_label, shift=UP))
            
            # 2. Move dot along the first line (Input -> Router)
            dot.move_to(line_in_to_router.get_start())
            self.play(dot.animate.move_to(line_in_to_router.get_end()), run_time=0.7)
            
            # 3. Router pulse (Processing)
            self.play(router_box.animate.set_stroke(width=8), run_time=0.1)
            self.play(router_box.animate.set_stroke(width=3), run_time=0.1)
            
            # 4. Move dot along the target line (Router -> Destination)
            dot.move_to(target_line.get_start())
            self.play(dot.animate.move_to(target_line.get_end()), run_time=0.7)
            
            # 5. Highlight destination box
            self.play(target_box.animate.set_color(PRIMARY_COLOR), run_time=0.2)
            self.play(
                FadeOut(dot), 
                FadeOut(query_label), 
                target_box.animate.set_color(GRID_COLOR),
                run_time=0.5
            )

        # Scenario A: To Knowledge Base
        route_packet('"How does cloud storage work?"', line_router_to_kb, kb_box)
        
        # Scenario B: To People
        route_packet('"Reset my cloud server password"', line_router_to_ppl, ppl_box)
        
        # Scenario C: To AI Agents
        route_packet('"Sync my photos to the cloud"', line_router_to_ai, ai_box)

        # Final emphasis
        footer = Text("Understanding intent ensures every query finds the right path.", 
                     font_size=18, color=PRIMARY_COLOR).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(footer))
        self.wait(2)

from manim import *

# Styling Constants
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink (for potential accents)
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light grey
FAILURE_COLOR = "#ef4444"      # Standard Red for 'X' marks

class KeywordMismatchScene(Scene):
    def construct(self):
        # Background set to White for high contrast with Black titles
        self.camera.background_color = WHITE

        # --- 1. TITLE SECTION ---
        # Requirement: Title set to BLACK and NOT bold
        title = Text("Keyword Search", color=BLACK, font_size=32, weight=NORMAL)
        title.to_edge(UP, buff=0.7)

        # --- 2. INPUT TEXT BLOCK ---
        input_label = Text("Given Text:", color=TEXT_COLOR, font_size=18)
        # Query using the primary pinkish-red theme
        input_query = Text(
            '"How can we lower our monthly infrastructure spend?"', 
            color=PRIMARY_COLOR, 
            font_size=24, 
            weight=BOLD
        )
        
        input_group = VGroup(input_label, input_query).arrange(DOWN, buff=0.2)
        input_group.shift(UP * 1.5)

        # --- 3. OPTIONS LIST ---
        option_font_size = 22

        opt1_text = Text("1. How to reduce cloud costs in AWS", color=TEXT_COLOR, font_size=option_font_size)
        opt2_text = Text("2. Best practices to reduce cloud costs", color=TEXT_COLOR, font_size=option_font_size)
        opt3_text = Text("3. Cloud cost optimization strategies", color=TEXT_COLOR, font_size=option_font_size)

        options_vgroup = VGroup(opt1_text, opt2_text, opt3_text).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        # Position options group clearly below the query block
        options_vgroup.shift(DOWN * 0.5)

        # --- 4. VISUAL CUES (RED X MARKS) ---
        # FIX: Using MathTex to handle the \times symbol correctly
        x_mark1 = MathTex(r"\times", color=FAILURE_COLOR).scale(1.2).next_to(opt1_text, RIGHT, buff=0.5)
        x_mark2 = MathTex(r"\times", color=FAILURE_COLOR).scale(1.2).next_to(opt2_text, RIGHT, buff=0.5)
        x_mark3 = MathTex(r"\times", color=FAILURE_COLOR).scale(1.2).next_to(opt3_text, RIGHT, buff=0.5)

        # --- ANIMATION SEQUENCE ---
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(input_group, shift=DOWN))
        self.wait(1)

        # Entry of options
        self.play(
            AnimationGroup(
                FadeIn(opt1_text, shift=RIGHT),
                FadeIn(opt2_text, shift=RIGHT),
                FadeIn(opt3_text, shift=RIGHT),
                lag_ratio=0.3
            )
        )
        self.wait(0.5)

        # Show RED X marks for ALL options (Keyword Failure)
        self.play(
            Write(x_mark1), 
            Write(x_mark2), 
            Write(x_mark3),
            run_time=1.5
        )
        
        # Final descriptive note
        note = Text(
            "Keyword Search Fails: No exact vocabulary overlap found.", 
            color=FAILURE_COLOR, 
            font_size=16, 
            slant=ITALIC
        )
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note))

        self.wait(3)

from manim import *

# Styling Constants
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light grey
FAILURE_COLOR = "#ef4444"      # Standard Red

class KeywordFailureScene(Scene):
    def construct(self):
        # Background color set to White for high contrast with Black titles
        self.camera.background_color = WHITE

        # --- 1. TITLE SECTION ---
        # Rule: Title is BLACK and NOT bold
        title = Text("Where Keyword Search Fails", color=BLACK, font_size=32, weight=NORMAL)
        title.to_edge(UP, buff=0.7)

        # --- 2. THE NEW QUERY BLOCK ---
        query_label = Text("New User Query:", color=TEXT_COLOR, font_size=18)
        query_text = Text(
            '"How can we lower our monthly infrastructure spend?"', 
            color=PRIMARY_COLOR, 
            font_size=24, 
            weight=BOLD
        )
        
        query_block = VGroup(query_label, query_text).arrange(DOWN, buff=0.2)
        query_block.shift(UP * 1.8)

        # --- 3. SIDE-BY-SIDE COMPARISON (Intent vs. Intent) ---
        # Sentence A (Intent Match 1)
        sent_a_box = RoundedRectangle(corner_radius=0.1, width=5.5, height=1.5, color=GRID_COLOR)
        sent_a_text = Text(
            "We need to reduce our\ncloud costs this quarter.", 
            color=TEXT_COLOR, font_size=18, line_spacing=0.8
        )
        group_a = VGroup(sent_a_box, sent_a_text)

        # Sentence B (Intent Match 2)
        sent_b_box = RoundedRectangle(corner_radius=0.1, width=5.5, height=1.5, color=GRID_COLOR)
        sent_b_text = Text(
            "Our infrastructure spending\nneeds to come down.", 
            color=TEXT_COLOR, font_size=18, line_spacing=0.8
        )
        group_b = VGroup(sent_b_box, sent_b_text)

        # Positioning the two intent examples
        comparison_row = VGroup(group_a, group_b).arrange(RIGHT, buff=0.8)
        comparison_row.shift(DOWN * 0.2)

        # --- 4. FAILURE ANALYSIS LABELS ---
        # Labeling the lack of overlap
        trad_label = Text(
            "Traditional Search: No Keyword Overlap", 
            color=FAILURE_COLOR, 
            font_size=20, 
            weight=BOLD
        )
        trad_label.next_to(comparison_row, DOWN, buff=0.6)

        # Dash line and unequal sign to show disconnect
        break_line = DashedLine(group_a.get_right(), group_b.get_left(), color=GRID_COLOR)
        # Using MathTex for the unequal symbol (Requires LaTeX/MikTeX)
        break_icon = MathTex(r"\neq", color=FAILURE_COLOR).scale(2).move_to(break_line.get_center())

        # --- 5. FOOTER ---
        footer_note = Text(
            "Keyword search sees words, not intent.", 
            color=TEXT_COLOR, font_size=16, slant=ITALIC
        )
        footer_note.to_edge(DOWN, buff=0.5)

        # --- ANIMATION SEQUENCE ---
        
        # Reveal Header and query
        self.play(Write(title))
        self.play(FadeIn(query_block, shift=DOWN))
        self.wait(1)

        # Show the comparison sentences (The boxes)
        self.play(
            Create(sent_a_box), Write(sent_a_text),
            Create(sent_b_box), Write(sent_b_text),
            run_time=2
        )
        self.wait(1)

        # Illustrate the disconnect
        self.play(Create(break_line), Write(break_icon))
        self.play(Write(trad_label))
        self.wait(1)

        # Final conclusion
        self.play(FadeIn(footer_note))
        self.wait(3)

from manim import *

# --- Configuration & Palette ---
PRIMARY_COLOR = "#db2777"     # Pinkish-Red
TEXT_COLOR = BLACK            # Standard high-contrast text
GRID_COLOR = "#e5e7eb"        # Light grey for arrows/lines
ACCENT_COLOR = "#be185d"      # Darker shade for emphasis

class CloudVectorRepresentation(Scene):
    def construct(self):
        # Rule 1b: Background set to WHITE
        self.camera.background_color = WHITE

        # --- 1. TITLE SECTION ---
        # Rule 1c: Title is BLACK and NOT bold
        title = Text("Contextual Vector Representation", color=BLACK, font_size=32, weight=NORMAL)
        title.to_edge(UP, buff=0.7)

        # --- 2. LAYOUT CONFIGURATION ---
        # We define fixed X-coordinates for strict vertical alignment of columns
        TXT_X = -4.8   # Starting point for Text (Left Aligned)
        ARR_X = -0.8   # Starting point for Arrows (Center Aligned)
        VEC_X = 1.0    # Starting point for Vectors (Left Aligned)

        # --- 3. ROW 1: SINGLE WORD ---
        word_cloud = Text('"Reduce cloud costs"', color=PRIMARY_COLOR, font_size=32, weight=BOLD)
        word_cloud.move_to([TXT_X, 1.5, 0], aligned_edge=LEFT)
        
        arrow_1 = Arrow(LEFT, RIGHT, color=GRID_COLOR).scale(0.7).move_to([ARR_X, 1.5, 0])
        
        vector_1 = MathTex(
            r"[ \ 0.21, \ -0.84, \ 1.32, \ 0.45, \ \dots \ ]",
            color=TEXT_COLOR
        ).scale(0.8).move_to([VEC_X, 1.5, 0], aligned_edge=LEFT)

        # --- 4. ROW 2: TECHNOLOGY CONTEXT ---
        context_tech = Text('"Minimize Spending"', color=TEXT_COLOR, font_size=24)
        context_tech.move_to([TXT_X, 0, 0], aligned_edge=LEFT)
        
        arrow_tech = Arrow(LEFT, RIGHT, color=GRID_COLOR).scale(0.7).move_to([ARR_X, 0, 0])
        
        vector_tech = MathTex(
            r"[ \ 0.89, \ 0.12, \ -0.44, \ 0.76, \ \dots \ ]",
            color=PRIMARY_COLOR
        ).scale(0.7).move_to([VEC_X, 0, 0], aligned_edge=LEFT)

        # --- 5. ROW 3: WEATHER CONTEXT ---
        context_weather = Text('"Rain cloud"', color=TEXT_COLOR, font_size=24)
        context_weather.move_to([TXT_X, -1.5, 0], aligned_edge=LEFT)
        
        arrow_weather = Arrow(LEFT, RIGHT, color=GRID_COLOR).scale(0.7).move_to([ARR_X, -1.5, 0])
        
        vector_weather = MathTex(
            r"[ \ -0.56, \ 0.98, \ 0.11, \ -0.23, \ \dots \ ]",
            color=PRIMARY_COLOR
        ).scale(0.7).move_to([VEC_X, -1.5, 0], aligned_edge=LEFT)

        # --- 6. ANIMATION SEQUENCE ---

        # Entrance
        self.play(Write(title))
        self.wait(0.5)

        # Row 1 Animation
        self.play(FadeIn(word_cloud, shift=RIGHT))
        self.play(GrowArrow(arrow_1))
        self.play(Write(vector_1))
        
        # Explanatory Note
        note = Text("Coordinates represent semantic meaning", color=ACCENT_COLOR, font_size=16, slant=ITALIC)
        note.next_to(vector_1, UP, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(note))
        self.wait(1.5)
        self.play(FadeOut(note))

        # Row 2 & 3 Sequential Reveal
        self.play(Write(context_tech), GrowArrow(arrow_tech), Write(vector_tech))
        self.wait(0.5)
        self.play(Write(context_weather), GrowArrow(arrow_weather), Write(vector_weather))
        
        # Highlight: Showing that the same word gets different numbers
        summary_label = Text(
            "The same word can have different vector representation based on intent & context.", 
            color=PRIMARY_COLOR, font_size=18
        ).to_edge(DOWN, buff=0.8)
        
        focus_box = SurroundingRectangle(VGroup(vector_tech, vector_weather), color=PRIMARY_COLOR, buff=0.2)
        
        self.play(Create(focus_box), Write(summary_label))
        self.wait(3)

from manim import *

# Styling Constants
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light grey

class HorizontalSentenceVector(Scene):
    def construct(self):
        # Set background to white for clarity and to support black text
        self.camera.background_color = WHITE

        # --- 1. TITLE SECTION ---
        # Requirement: BLACK and NOT bold
        title = Text("Sentence to Vector Mapping", color=BLACK, font_size=32, weight=NORMAL)
        title.to_edge(UP, buff=0.7)

        # --- 2. COMPONENTS (DEFINED FOR LEFT-TO-RIGHT FLOW) ---
        
        # A. The Input Sentence
        sentence_box = RoundedRectangle(corner_radius=0.1, width=4.5, height=1.2, color=GRID_COLOR)
        sentence_text = Text(
            '"We need to reduce\ncloud costs."', 
            color=PRIMARY_COLOR, 
            font_size=18,
            line_spacing=0.6,
            weight=BOLD
        )
        input_group = VGroup(sentence_box, sentence_text)

        # B. The Embedding Engine (Center Piece)
        engine_box = Rectangle(width=2.5, height=1.5, color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=0.1)
        engine_label = Text("Embedding\nEngine", color=PRIMARY_COLOR, font_size=16, weight=BOLD)
        engine_label.move_to(engine_box.get_center())
        engine_group = VGroup(engine_box, engine_label)

        # C. The Horizontal Vector
        # FIX: Vector is now horizontal [ x, y, z ... ]
        vector_math = MathTex(
            r"[ \ 0.54, \ -0.12, \ 0.89, \ 0.31, \ \dots \ ]",
            color=TEXT_COLOR
        ).scale(0.8)
        vector_frame = RoundedRectangle(corner_radius=0.1, width=5, height=1.2, color=TEXT_COLOR)
        vector_group = VGroup(vector_frame, vector_math)

        # --- 3. LAYOUT ENGINE (HORIZONTAL) ---
        # Group everything and arrange with a strict buffer to prevent any overlap
        main_flow = VGroup(input_group, engine_group, vector_group).arrange(RIGHT, buff=0.8)
        main_flow.move_to(ORIGIN)

        # Connectors (Arrows between the boxes)
        arrow1 = Arrow(input_group.get_right(), engine_group.get_left(), color=GRID_COLOR, buff=0.1)
        arrow2 = Arrow(engine_group.get_right(), vector_group.get_left(), color=PRIMARY_COLOR, buff=0.1)

        # Labels for the sections (Bottom positioned to avoid overlapping boxes)
        input_tag = Text("Input Sentence", color=TEXT_COLOR, font_size=14).next_to(input_group, DOWN, buff=0.3)
        output_tag = Text("Semantic Vector", color=TEXT_COLOR, font_size=14).next_to(vector_group, DOWN, buff=0.3)

        # --- ANIMATION SEQUENCE ---

        # Step 1: Reveal Title and Input
        self.play(Write(title))
        self.play(FadeIn(input_group, shift=RIGHT), FadeIn(input_tag))
        self.wait(1)

        # Step 2: Transition through the Engine
        self.play(Create(engine_group), GrowArrow(arrow1))
        self.wait(0.5)

        # Step 3: Reveal the Horizontal Vector
        # We animate the arrow and the vector appearing together
        self.play(
            GrowArrow(arrow2),
            FadeIn(vector_group, shift=RIGHT),
            FadeIn(output_tag),
            run_time=1.5
        )
        
        # Step 4: Final visual highlight on the connection
        self.play(
            engine_box.animate.set_stroke(width=6),
            vector_math.animate.set_color(PRIMARY_COLOR),
            run_time=0.4
        )
        self.play(
            engine_box.animate.set_stroke(width=2),
            vector_math.animate.set_color(TEXT_COLOR),
            run_time=0.4
        )

        self.wait(3)