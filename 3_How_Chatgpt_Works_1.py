from manim import *

# Define the custom color palette
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = "#fce7f3" # Very Light Pink
ACCENT_COLOR = "#be185d"    # Darker Pink
TEXT_COLOR = "#1f2937"      # Dark Grey/Black
GRID_COLOR = "#e5e7eb"      # Light grey

class MathematicalMapping(Scene):
    def construct(self):
        # Set background to white
        self.camera.background_color = WHITE

        # --- PHASE 1: Top Abstraction Layer ---
        eq_f = MathTex("f", color=TEXT_COLOR).scale(1.5)
        eq_lp = MathTex("(", color=TEXT_COLOR).scale(1.5)
        eq_x = MathTex("x", color=TEXT_COLOR).scale(1.5)
        eq_rp = MathTex(")", color=TEXT_COLOR).scale(1.5)
        eq_eq = MathTex("=", color=TEXT_COLOR).scale(1.5)
        eq_y = MathTex("y", color=TEXT_COLOR).scale(1.5)

        top_eq = VGroup(eq_f, eq_lp, eq_x, eq_rp, eq_eq, eq_y).arrange(RIGHT, buff=0.2)
        top_eq.to_edge(UP, buff=1)

        self.play(Write(top_eq))
        self.wait(1)

        # --- PHASE 2: Implementation Elements (Initially Invisible) ---

        # 1. Representing 'x' (Input Text)
        input_data = Text("The cat sat on the", font_size=24, color=TEXT_COLOR)
        
        # 2. Representing 'f' (Neural Network)
        layers = [3, 5, 5, 3]
        nn_nodes = VGroup()
        nn_edges = VGroup()
        for i, num_nodes in enumerate(layers):
            layer = VGroup(*[Dot(radius=0.08, color=PRIMARY_COLOR) for _ in range(num_nodes)])
            layer.arrange(DOWN, buff=0.2)
            nn_nodes.add(layer)
        nn_nodes.arrange(RIGHT, buff=0.45)

        for i in range(len(layers) - 1):
            for node_a in nn_nodes[i]:
                for node_b in nn_nodes[i+1]:
                    edge = Line(node_a.get_center(), node_b.get_center(), 
                                stroke_width=0.5, stroke_opacity=0.2, color=ACCENT_COLOR)
                    nn_edges.add(edge)
        
        nn_model = VGroup(nn_edges, nn_nodes)

        # 3. Representing 'y' (Bar Chart)
        chart = BarChart(
            values=[0.85, 0.10, 0.05],
            bar_names=["mat", "floor", "rug"],
            y_range=[0, 1, 0.5],
            y_length=2.5,
            x_length=3.5,
            x_axis_config={"color": TEXT_COLOR, "include_numbers": False},
            y_axis_config={"color": TEXT_COLOR},
            bar_colors=[PRIMARY_COLOR, ACCENT_COLOR, SECONDARY_COLOR],
        )

        # --- PHASE 3: Arranging the Representation Layer ---
        # Symbols for the representation layer
        rep_lp = eq_lp.copy()
        rep_rp = eq_rp.copy()
        rep_eq = eq_eq.copy()

        # Grouping them to ensure proper spacing
        representation_group = VGroup(
            nn_model, rep_lp, input_data, rep_rp, rep_eq, chart
        ).arrange(RIGHT, buff=0.4)
        
        representation_group.center().shift(DOWN * 0.5)

        # --- PHASE 4: Animation Sequence ---

        # x -> Input Text
        self.play(
            ReplacementTransform(eq_x.copy(), input_data),
            ReplacementTransform(eq_lp.copy(), rep_lp),
            ReplacementTransform(eq_rp.copy(), rep_rp),
            run_time=1.5
        )
        self.wait(0.3)

        # f -> Neural Network
        self.play(
            ReplacementTransform(eq_f.copy(), nn_model),
            run_time=1.5
        )
        self.wait(0.3)

        # y -> Bar Chart
        self.play(
            ReplacementTransform(eq_eq.copy(), rep_eq),
            ReplacementTransform(eq_y.copy(), chart),
            run_time=1.5
        )

        # Final Highlight: Probability labels
        # Correctly accessing chart labels for styling
        for bar_label in chart.get_x_axis():
            if hasattr(bar_label, "set_color"):
                bar_label.set_color(TEXT_COLOR)

        conf_text = Text(" Max Probability: 85%", font_size=22, color=PRIMARY_COLOR)
        conf_text.next_to(chart, DOWN, buff=0.5)
        self.play(Write(conf_text))

        self.wait(3)

from manim import *
import random

# Define the custom color palette
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = "#fce7f3" # Very Light Pink
ACCENT_COLOR = "#be185d"    # Darker Pink
TEXT_COLOR = "#1f2937"      # Dark Grey/Black
GRID_COLOR = "#e5e7eb"      # Light grey

class MultiColumnVocabularyScroll(Scene):
    def construct(self):
        # Set background to white
        self.camera.background_color = WHITE
        # Set a fixed seed for reproducible random generation
        random.seed(42)

        # --- 1. LEFT SIDE: CONTEXT & PLACEHOLDER ---
        sentence = Text("The cat sat on the", font_size=32, color=TEXT_COLOR)
        placeholder_line = Line(LEFT, RIGHT, color=PRIMARY_COLOR, stroke_width=3).set_width(1.5)
        
        left_group = VGroup(sentence, placeholder_line).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        # Anchor strictly to the left edge
        left_group.to_edge(LEFT, buff=0.8).shift(UP * 0.5)

        self.play(Write(sentence))
        self.play(Create(placeholder_line))
        self.wait(0.5)

        # --- 2. RIGHT SIDE: MULTI-COLUMN SCROLL ---
        targets = ["mat", "floor", "rug"]
        fillers = [
            "apple", "book", "cloud", "desk", "echo", "forest", "gate", "hill", 
            "ice", "jump", "kite", "lamp", "moon", "note", "ocean", "page", 
            "quill", "star", "tree", "unit", "view", "wall", "xenon", "yard", 
            "zone", "bread", "chair", "data", "engine", "field", "glass"
        ]
        
        num_cols = 5
        words_per_col = 40 # Increased word count for a denser look
        master_scroll_group = VGroup()

        for _ in range(num_cols):
            col_word_list = random.choices(fillers, k=words_per_col)
            # Ensure at least a few targets appear in every column
            for target in targets:
                for _ in range(2): # Insert each target twice per column
                    insert_idx = random.randint(0, len(col_word_list))
                    col_word_list.insert(insert_idx, target)
            
            col_texts = []
            for word in col_word_list:
                is_target = word in targets
                t = Text(
                    word, 
                    font_size=16, # Compact size to fit 5-6 columns
                    color=PRIMARY_COLOR if is_target else TEXT_COLOR,
                    weight=BOLD if is_target else LIGHT,
                    fill_opacity=1 if is_target else 0.5 # Dim non-targets for clarity
                )
                col_texts.append(t)
            
            col_vg = VGroup(*col_texts).arrange(DOWN, buff=0.35)
            master_scroll_group.add(col_vg)

        # Arrange columns and anchor them to the RIGHT
        master_scroll_group.arrange(RIGHT, buff=0.6)
        master_scroll_group.to_edge(RIGHT, buff=0.5)
        
        # Calculate vertical path: Start below screen, end above screen
        scroll_height = master_scroll_group.height
        # Start completely below the bottom edge
        start_pos = master_scroll_group.get_center() + DOWN * (scroll_height/2 + config.frame_height/2 + 2)
        master_scroll_group.move_to(start_pos)

        # Total distance to clear the top edge
        shift_dist = scroll_height + config.frame_height + 4

        # Action: Scrolling on the right side only
        self.play(
            master_scroll_group.animate.shift(UP * shift_dist),
            run_time=7, # Slightly slower to see the targets
            rate_func=linear
        )
        self.remove(master_scroll_group)

        # --- 3. RIGHT SIDE: PROBABILITY CHART ---
        chart = BarChart(
            values=[0.85, 0.10, 0.03],
            y_range=[0, 1, 0.5],
            y_length=2.5,
            x_length=4.0,
            x_axis_config={"color": TEXT_COLOR, "stroke_width": 1},
            y_axis_config={"color": TEXT_COLOR, "stroke_width": 1},
            bar_colors=[PRIMARY_COLOR, ACCENT_COLOR, SECONDARY_COLOR],
        )
        # Position the chart exactly where the scroll was
        chart.to_edge(RIGHT, buff=1.0).shift(DOWN * 0.5)

        labels = VGroup(
            Text("mat", font_size=20, color=TEXT_COLOR),
            Text("floor", font_size=20, color=TEXT_COLOR),
            Text("rug", font_size=20, color=TEXT_COLOR)
        )
        for i, label in enumerate(labels):
            label.next_to(chart.bars[i], DOWN, buff=0.2)

        self.play(Create(chart), Write(labels), run_time=1.5)

        # --- 4. THE RESOLUTION ---
        # The winning word moves from the chart to the left sentence
        final_mat = Text("mat", font_size=32, color=PRIMARY_COLOR)
        final_mat.next_to(placeholder_line, UP, buff=0.1)

        self.play(
            ReplacementTransform(labels[0].copy(), final_mat),
            Indicate(chart.bars[0], color=PRIMARY_COLOR, scale_factor=1.1),
            run_time=1.5
        )

        self.wait(3)


from manim import *

# Styling Constants
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
TEXT_COLOR = "#1f2937"      # Dark Grey/Black

class TokenizationFinalFixed(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # 1. DATA PREPARATION
        data = [
            ("The", "464"),
            ("cat", "3797"),
            ("sat", "3332"),
            ("on", "319"),
            ("the", "262")
        ]

        # 2. LABELS (Strictly black and not bold as per rules)
        human_label = Text("Human Language", font_size=24, color=TEXT_COLOR, weight=NORMAL)
        human_label.to_edge(UP, buff=1.0)
        
        machine_label = Text("Machine IDs", font_size=24, color=TEXT_COLOR, weight=NORMAL)
        machine_label.to_edge(DOWN, buff=1.0)

        # 3. BUILD THE TOKEN UNITS
        token_units = VGroup()

        for word, id_val in data:
            # Create text objects
            w_text = Text(word, font_size=32, color=TEXT_COLOR)
            i_text = Text(id_val, font_size=32, color=PRIMARY_COLOR, weight=BOLD)
            
            # CALCULATE BOX: Ensure it fits the larger element
            b_width = max(w_text.width, i_text.width) + 0.6
            b_height = 1.0
            
            box = RoundedRectangle(
                corner_radius=0.1,
                width=b_width,
                height=b_height,
                color=PRIMARY_COLOR,
                stroke_width=2
            )
            
            # Position word at center
            w_text.move_to(box.get_center())
            
            # Position ID far ABOVE the box and make it invisible
            i_text.move_to(box.get_center() + UP * 1.5).set_opacity(0)
            
            # Unit Group: [0] Box, [1] Word, [2] ID
            unit = VGroup(box, w_text, i_text)
            token_units.add(unit)

        # 4. INITIAL LAYOUT (Sentence Mode)
        token_units.arrange(RIGHT, buff=0.1).center()

        # --- ANIMATION SEQUENCE ---

        # Phase 1: Show the Sentence
        self.play(FadeIn(human_label, shift=DOWN*0.3))
        self.play(Create(token_units, lag_ratio=0.1), run_time=1.5)
        self.wait(1)

        # Phase 2: Split apart (FIXED: Using .animate to avoid VGroup error)
        self.play(
            token_units.animate.arrange(RIGHT, buff=0.8).center(),
            run_time=1.2
        )
        self.wait(0.5)

        # Phase 3: THE ZERO-OVERLAP SLIDE
        self.play(FadeIn(machine_label, shift=UP*0.3))
        
        # We process each unit: Word slides DOWN out, ID slides DOWN in.
        self.play(
            *[
                Succession(
                    # 1. Word slides out of the bottom and disappears
                    unit[1].animate.shift(DOWN * 1).set_opacity(0),
                    # 2. ID slides from the top into the center and appears
                    unit[2].animate.move_to(unit[0].get_center()).set_opacity(1),
                )
                for unit in token_units
            ],
            run_time=2.5
        )

        # Final Success Pulse
        self.play(
            token_units.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=0.8
        )

        self.wait(2)

from manim import *
import random

# --- Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Phone outline & highlight)
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink (Suggestions & bubbles)
SCREEN_BG_COLOR = WHITE        
TEXT_COLOR = "#1f2937"         
KEY_COLOR = "#e5e7eb"          

class MobileTypingRefined(Scene):
    def construct(self):
        # Ensure the camera background is strictly white
        self.camera.background_color = WHITE

        # --- 0. AMBIENT BACKGROUND PARTICLES ---
        particles = VGroup()
        for _ in range(25):
            radius = random.uniform(0.05, 0.15)
            particle = Circle(
                radius=radius, 
                fill_color=PRIMARY_COLOR, 
                fill_opacity=random.uniform(0.1, 0.2), 
                stroke_width=0
            )
            particle.move_to([random.uniform(-7, 7), random.uniform(-4, 4), 0])
            velocity = np.array([random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0])
            particle.add_updater(lambda m, dt, v=velocity: m.shift(v * dt))
            particles.add(particle)
        
        self.add(particles)

        # --- 1. PHONE STRUCTURE ---
        # Outline is #db2777
        phone_frame = RoundedRectangle(
            corner_radius=0.4, height=7.8, width=4.2,
            fill_color=PRIMARY_COLOR, fill_opacity=1, stroke_width=0
        ).set_z_index(1)
        
        screen = RoundedRectangle(
            corner_radius=0.2, height=7.4, width=3.9,
            fill_color=SCREEN_BG_COLOR, fill_opacity=1, stroke_width=0
        ).move_to(phone_frame.get_center()).set_z_index(2)

        # --- 2. SCREEN CONTENT (CAT IMAGE) ---
        try:
            cat_photo = ImageMobject("cat.png") 
            cat_photo.width = 3.3
            cat_photo.move_to(screen.get_top() + DOWN * 1.6)
        except:
            cat_photo = RoundedRectangle(height=2.2, width=3.3, color=GRAY, fill_opacity=0.1)
            cat_photo.move_to(screen.get_top() + DOWN * 1.6)
        cat_photo.set_z_index(3)

        # Input box with subtle stroke
        input_box = RoundedRectangle(
            corner_radius=0.1, height=0.6, width=3.5,
            fill_color=WHITE, fill_opacity=1, stroke_color=LIGHT_GREY, stroke_width=1.5
        ).next_to(cat_photo, DOWN, buff=0.4).set_z_index(3)

        # --- 3. KEYBOARD ---
        keyboard_group = VGroup()
        rows = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M"]
        ]

        for row in rows:
            row_group = VGroup()
            for letter in row:
                key_bg = RoundedRectangle(corner_radius=0.05, height=0.45, width=0.32, 
                                        fill_color=KEY_COLOR, fill_opacity=1, stroke_width=0)
                char = Text(letter, font_size=16, color=TEXT_COLOR)
                row_group.add(VGroup(key_bg, char))
            row_group.arrange(RIGHT, buff=0.06)
            keyboard_group.add(row_group)
        
        keyboard_group.arrange(DOWN, buff=0.1)
        space_bar = RoundedRectangle(corner_radius=0.05, height=0.4, width=2.0, 
                                   fill_color=KEY_COLOR, fill_opacity=1, stroke_width=0)
        full_keyboard = VGroup(keyboard_group, space_bar).arrange(DOWN, buff=0.1)
        full_keyboard.move_to(screen.get_bottom() + UP * 1.3).set_z_index(3)

        # --- 4. PREDICTIVE SUGGESTIONS ---
        suggestion_words = ["mat", "rug", "floor"]
        suggestions = VGroup()
        for word in suggestion_words:
            bg = RoundedRectangle(corner_radius=0.1, height=0.5, width=1.1, 
                                fill_color=SECONDARY_COLOR, fill_opacity=1, stroke_width=0)
            label = Text(word, font_size=18, color=PRIMARY_COLOR)
            suggestions.add(VGroup(bg, label))
        
        suggestions.arrange(RIGHT, buff=0.15).next_to(full_keyboard, UP, buff=0.2)
        suggestions.set_opacity(0).set_z_index(3)

        # --- 5. ANIMATION LOGIC ---
        self.add(phone_frame, screen)
        self.play(FadeIn(cat_photo), FadeIn(full_keyboard), Create(input_box))
        
        # FIXED: Start with the first letter to avoid empty mobject coordinates
        target_sentence = "The cat sat on the "
        text_anchor = input_box.get_left() + RIGHT * 0.25
        
        # Initial Mobject
        displayed_text = Text(target_sentence[0], font_size=20, color=TEXT_COLOR)
        displayed_text.move_to(text_anchor, LEFT).set_z_index(5)
        self.add(displayed_text)

        # Typing loop
        for i in range(2, len(target_sentence) + 1):
            partial = target_sentence[:i]
            # Create new text mobject
            new_text = Text(partial, font_size=20, color=TEXT_COLOR)
            new_text.move_to(text_anchor, LEFT).set_z_index(5)
            
            # Use Transform to move points smoothly
            self.play(Transform(displayed_text, new_text), run_time=0.07, rate_func=linear)
            
            if partial == "The cat sat on the ":
                self.play(suggestions.animate.set_opacity(1), run_time=0.4)

        # Highlight 'mat'
        self.play(
            suggestions[0][0].animate.set_fill(PRIMARY_COLOR),
            suggestions[0][1].animate.set_color(WHITE),
            run_time=0.3
        )

        # Final word completion
        final_sentence = "The cat sat on the mat"
        final_text = Text(final_sentence, font_size=20, color=TEXT_COLOR)
        final_text.move_to(text_anchor, LEFT).set_z_index(5)
        
        self.play(Transform(displayed_text, final_text), run_time=0.2)
        
        self.wait(3)

from manim import *

# --- Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
TEXT_COLOR = "#1f2937"         # Dark Grey
GRID_COLOR = "#e5e7eb"         # Light Grey
BG_COLOR = WHITE

class EmbeddingLookupClean(Scene):
    def construct(self):
        # Setting a clean, pure white background
        self.camera.background_color = BG_COLOR

        # --- 1. MINIMAL HEADER (Top of Screen) ---
        id_val = Text("ID: 3797", font_size=20, color=TEXT_COLOR)
        cat_sub = Text("(cat)", font_size=16, color=PRIMARY_COLOR, slant=ITALIC).next_to(id_val, RIGHT, buff=0.15)
        header = VGroup(id_val, cat_sub).to_edge(UP, buff=0.2)

        # --- 2. EMBEDDING MATRIX E ---
        matrix_w, matrix_h = 3.2, 5.0
        matrix_frame = Rectangle(height=matrix_h, width=matrix_w, color=GRID_COLOR, fill_color="#fcfcfc", fill_opacity=1)
        matrix_label = MathTex("E", color=BLACK, font_size=36).next_to(matrix_frame, UP, buff=0.15)
        
        # Matrix Rows
        num_rows = 18
        rows = VGroup(*[
            Line(LEFT, RIGHT, color=GRID_COLOR, stroke_width=1).scale(1.4)
            for _ in range(num_rows)
        ]).arrange(DOWN, buff=0.25).move_to(matrix_frame)
        
        # Shifted left for clear layout
        matrix_group = VGroup(matrix_frame, matrix_label, rows).shift(LEFT * 2.5 + DOWN * 0.3)

        # --- 3. THE SCAN FILTER ---
        scan_bar = Rectangle(
            height=0.15, width=matrix_w, 
            fill_color=PRIMARY_COLOR, fill_opacity=0.2, 
            stroke_width=0
        ).move_to(matrix_frame.get_top())

        target_idx = 7
        target_y = rows[target_idx].get_y()
        
        # The row to be extracted
        extract_row = rows[target_idx].copy().set_color(PRIMARY_COLOR).set_stroke(width=4)
        row_label = Text("Row 3797", font_size=14, color=PRIMARY_COLOR).next_to(matrix_frame, LEFT, buff=0.3)
        row_label.set_y(target_y)

        # --- 4. THE CONCEPT VECTOR (Resulting Column) ---
        vector_w, vector_h = 1.0, 5.5
        vector_rect = Rectangle(height=vector_h, width=vector_w, color=PRIMARY_COLOR, fill_color=WHITE, fill_opacity=1)
        vector_rect.shift(RIGHT * 1.5 + DOWN * 0.3) # Centered-right layout
        
        vector_title = Text("Concept Vector", font_size=20, color=BLACK).next_to(vector_rect, UP, buff=0.25)
        dim_label = Text("12,288 Dimensions", font_size=16, color=PRIMARY_COLOR).next_to(vector_rect, DOWN, buff=0.25)

        # Numerical Data (Top 3, Ellipsis, Bottom 2)
        numerical_data = VGroup(
            Text("0.60", font_size=14, color=TEXT_COLOR),
            Text("-0.81", font_size=14, color=TEXT_COLOR),
            Text("-0.69", font_size=14, color=TEXT_COLOR),
            MathTex("\\vdots", color=TEXT_COLOR, font_size=28),
            Text("0.99", font_size=14, color=TEXT_COLOR),
            Text("0.51", font_size=14, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.45).move_to(vector_rect)

        # --- 5. ANIMATION SEQUENCE ---
        self.play(FadeIn(header, shift=UP), FadeIn(matrix_group, shift=DOWN))
        self.wait(0.2)

        # Step 1: Scanning
        self.add(scan_bar)
        self.play(scan_bar.animate.set_y(target_y), run_time=1.0, rate_func=rate_functions.smooth)
        self.play(
            Create(extract_row),
            Write(row_label),
            FadeOut(scan_bar)
        )
        self.wait(0.3)

        # Step 2: Extraction Animation (The "Fixed" Transition)
        # Sequence: Detach -> Move & Rotate -> Expand into Rectangle
        self.play(
            FadeOut(row_label),
            header.animate.set_color(PRIMARY_COLOR),
            extract_row.animate.move_to(vector_rect.get_center()).rotate(PI/2).set_length(vector_h),
            run_time=1.2,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # Step 3: Expand the line into the full vector box
        self.play(
            ReplacementTransform(extract_row, vector_rect),
            Write(vector_title),
            run_time=0.6
        )

        # Step 4: Populate with numerical values
        self.play(
            FadeIn(numerical_data, lag_ratio=0.1, shift=UP),
            Write(dim_label),
            run_time=1.0
        )

        # Step 5: Final conceptual explanation
        brace = Brace(vector_rect, RIGHT, color=PRIMARY_COLOR, buff=0.2)
        brace_text = Text("This vector represents\nthe 'meaning' of a cat", font_size=14, color=PRIMARY_COLOR).next_to(brace, RIGHT)
        
        self.play(GrowFromCenter(brace), Write(brace_text))
        self.wait(3)

from manim import *
import numpy as np

# --- Color Palette ---
PRIMARY_COLOR = "#f40b74"      # Pinkish-Red (Cat)
KITTEN_COLOR = "#bc0853"       # Darker Pink (Kitten)
DOG_COLOR = "#bd5c84"          # Muted Pink (Dog)
TOASTER_COLOR = "#c993aa"      # Light Pinkish-Grey (Toaster)
TEXT_COLOR = "#1f2937"
AXIS_COLOR = "#9ca3af"
BG_COLOR = WHITE

class ThreeDWordEmbeddings(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # --- 1. 3D AXES ---
        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=5, y_length=5, z_length=5,
            axis_config={"color": AXIS_COLOR, "stroke_width": 2}
        )
        
        # Initial Camera Angle
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # --- 2. VECTOR DATA WITH CUSTOM OFFSETS ---
        # I've added specific 'offset' vectors to manually space out the labels,
        # preventing overlap between close concepts like "Cat" and "Kitten".
        concept_data = [
            {
                "label": "Cat", "pos": [2, 2, 1], "color": PRIMARY_COLOR,
                "offset": UP * 0.9 + RIGHT * 1.3  # Push Cat up and left
            },
            {
                "label": "Kitten", "pos": [2.1, 1.8, 0.8], "color": KITTEN_COLOR,
                "offset": DOWN * 0.4 + RIGHT * 1.9 # Push Kitten down and right
            },
            {
                "label": "Dog", "pos": [1.2, 0.5, 2.5], "color": DOG_COLOR,
                "offset": UP * 0.5 + RIGHT * 0.3 # Push Dog further up
            },
            {
                "label": "Toaster", "pos": [-2, -1.5, 0.5], "color": TOASTER_COLOR,
                "offset": DOWN * 0.5 + LEFT * 0.9 # Push Toaster down
            },
        ]

        vectors = VGroup()
        labels = VGroup()

        for data in concept_data:
            # Create 3D Arrow
            vec = Arrow3D(
                start=ORIGIN, 
                end=np.array(data["pos"]), 
                color=data["color"],
                resolution=8
            )
            vectors.add(vec)
            
            # Create Label using custom offset
            label = Text(data["label"], font_size=20, color=data["color"])
            # Apply the specific offset for this concept
            label.move_to(vec.get_end() + data["offset"])
            labels.add(label)

        # --- 3. ANIMATION SEQUENCE ---
        self.play(Create(axes), run_time=1.5)
        self.wait(0.5)

        # Add vectors and fix labels to face camera
        for i in range(len(vectors)):
            self.play(Create(vectors[i]), FadeIn(labels[i]), run_time=1)
            # This is the key: it anchors labels to 3D space but keeps them facing front
            self.add_fixed_orientation_mobjects(labels[i])
            self.wait(0.1)

        self.wait(1)

        # --- 4. SEMANTIC ROTATION ---
        # Labels will now move with the vectors and stay perfectly legible and spaced
        self.move_camera(theta=-225 * DEGREES, run_time=6, rate_func=linear)
        self.wait(2)

from manim import *
import numpy as np

# --- Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Highlighter & Now Vector Color)
SECONDARY_COLOR = "#fce7f3"    # Light Pink
TEXT_COLOR = "#1f2937"         # Dark Grey (for standard text)
WHITE_TEXT = BLACK             # For text on dark background
AXIS_COLOR = "#9ca3af"         # Grey for grid
# UPDATED: Vector color changed from BLUE to PRIMARY_COLOR
VECTOR_COLOR = PRIMARY_COLOR   
ERROR_COLOR = RED              # Red for the error text
BG_COLOR = WHITE               # Clean background

class ContextProblemRefined(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- 1. HEADER ---
        id_val = Text("ID: 3797", font_size=20, color=WHITE_TEXT)
        cat_sub = Text("(cat)", font_size=16, color=PRIMARY_COLOR, slant=ITALIC).next_to(id_val, RIGHT, buff=0.15)
        header = VGroup(id_val, cat_sub).to_edge(UP, buff=0.2)
        self.add_fixed_in_frame_mobjects(header)

        # --- 2. 3D AXES SETUP ---
        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=5, y_length=5, z_length=5,
            axis_config={"color": AXIS_COLOR, "stroke_width": 2}
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # --- 3. THE PHRASES (Fixed 2D Overlay) ---
        phrase_1 = VGroup(
            Text("House ", font_size=24, color=WHITE_TEXT),
            # Color updated to VECTOR_COLOR (Pink)
            Text("cat", font_size=24, color=VECTOR_COLOR, weight=BOLD)
        ).arrange(RIGHT, buff=0.1)

        phrase_2 = VGroup(
            # Color updated to VECTOR_COLOR (Pink)
            Text("Cat ", font_size=24, color=VECTOR_COLOR, weight=BOLD),
            Text("Fish", font_size=24, color=WHITE_TEXT)
        ).arrange(RIGHT, buff=0.1)

        phrases = VGroup(phrase_1, phrase_2).arrange(DOWN, buff=0.8)
        phrases.to_edge(LEFT, buff=0.8).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(phrases)

        # --- 4. THE STATIC VECTOR ---
        static_pos = [2, 2, 1]
        static_vec = Arrow3D(
            start=ORIGIN, 
            end=np.array(static_pos), 
            color=VECTOR_COLOR, # Now Pink
            resolution=8
        )
        
        # Static label anchored to the tip
        vec_label = Text("Vector 3797", font_size=18, color=VECTOR_COLOR)
        vec_label.move_to(static_vec.get_end() + OUT * 0.3)

        # --- 5. ANIMATION SEQUENCE ---
        self.play(Create(axes), FadeIn(phrases, shift=RIGHT), run_time=1.5)
        self.wait(0.5)

        # Action: Both "cat" words show they map to the same pink vector
        self.play(
            Indicate(phrase_1[1], color=VECTOR_COLOR, scale_factor=1.2), 
            Indicate(phrase_2[0], color=VECTOR_COLOR, scale_factor=1.2)
        )
        self.play(Create(static_vec), Write(vec_label))
        self.add_fixed_orientation_mobjects(vec_label)
        self.wait(1)

        # Action: Show Ambiguous Mapping text (Cross removed)
        error_text = Text("Ambiguous Mapping", font_size=20, color=ERROR_COLOR)
        # FIXED ALIGNMENT: aligned_edge=LEFT ensures it aligns with the phrases above
        error_text.next_to(phrases, DOWN, buff=0.8, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(error_text)
        self.play(Write(error_text))
        self.wait(1.5)

        # Phase 2 Transition: Highlight context words
        self.play(
            FadeOut(error_text),
            # Highlight "House" and "scan" as the solution modifiers
            phrase_1[0].animate.set_color(PRIMARY_COLOR).scale(1.1),
            phrase_2[1].animate.set_color(PRIMARY_COLOR).scale(1.1),
            run_time=1
        )

        # Symbolic "Attention" connections
        line_1 = Line(phrase_1[0].get_right(), phrase_1[1].get_left(), color=PRIMARY_COLOR, stroke_width=2)
        line_2 = Line(phrase_2[1].get_left(), phrase_2[0].get_right(), color=PRIMARY_COLOR, stroke_width=2)
        self.add_fixed_in_frame_mobjects(line_1, line_2)
        
        self.play(Create(line_1), Create(line_2), rate_func=smooth)
        self.wait(2)

from manim import *

# --- Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (The Context-Aware Glow)
STATIC_VECTOR_COLOR = BLUE     # Blue (Initial Static Vectors)
TRANSFORMER_BOX_COLOR = "#4b5563" # Gray (The Transformer Block)
TEXT_COLOR = BLACK
BG_COLOR = WHITE               # Clean Black Background

class TransformerBlockIntro(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- 1. HEADER ---
        # Minimalist title at the top
        title = Text("Phase 2: The Transformer Block", font_size=28, color=TEXT_COLOR, weight=NORMAL)
        title.to_edge(UP, buff=0.5)

        # --- 2. THE TRANSFORMER BLOCK (CENTRAL HUB) ---
        transformer_box = RoundedRectangle(
            corner_radius=0.2, height=3.5, width=5.0,
            fill_color=TRANSFORMER_BOX_COLOR, fill_opacity=0.4,
            stroke_color=GRAY, stroke_width=2
        )
        box_label = Text("Transformer Block", font_size=24, color=GRAY).next_to(transformer_box, UP, buff=0.2)
        
        # Sub-labels for the mechanism
        mechanism_label = Text("Context Processing", font_size=16, color=GRAY_B).move_to(transformer_box.get_center())
        
        transformer_group = VGroup(transformer_box, box_label, mechanism_label).shift(DOWN * 0.5)

        # --- 3. THE WORD VECTORS (INPUT & OUTPUT) ---
        words = ["The", "cat", "sat", "on", "the"]
        
        # Helper to create a vector stack
        def create_vector_stack(color, opacity=1.0):
            return VGroup(*[
                Rectangle(height=1.2, width=0.25, fill_color=color, fill_opacity=opacity, stroke_width=1)
                for _ in range(5)
            ]).arrange(RIGHT, buff=0.4)

        # Input: 5 Static Blue Vectors
        input_vectors = create_vector_stack(STATIC_VECTOR_COLOR)
        input_labels = VGroup(*[
            Text(word, font_size=18, color=STATIC_VECTOR_COLOR)
            for word in words
        ])
        for i, label in enumerate(input_labels):
            label.next_to(input_vectors[i], DOWN, buff=0.2)
        
        input_group = VGroup(input_vectors, input_labels).to_edge(LEFT, buff=1.0)

        # Output: 5 Glowing Context-Aware Vectors (using PRIMARY_COLOR)
        output_vectors = create_vector_stack(PRIMARY_COLOR)
        # Adding a glow effect for the context-aware state
        glow_vectors = output_vectors.copy().set_stroke(PRIMARY_COLOR, width=8, opacity=0.3)
        
        output_labels = VGroup(*[
            Text(word, font_size=18, color=PRIMARY_COLOR)
            for word in words
        ])
        for i, label in enumerate(output_labels):
            label.next_to(output_vectors[i], DOWN, buff=0.2)
            
        output_group = VGroup(output_vectors, glow_vectors, output_labels).to_edge(RIGHT, buff=1.0)

        # --- 4. ANIMATION SEQUENCE ---
        self.play(FadeIn(title, shift=DOWN), FadeIn(transformer_group, shift=UP))
        self.wait(0.5)

        # Action: 5 Blue vectors enter the gray box
        self.play(Write(input_labels))
        self.play(Create(input_vectors), run_time=1.0)
        self.wait(0.2)

        self.play(
            input_group.animate.move_to(transformer_box.get_center()).scale(0.5).set_opacity(0),
            mechanism_label.animate.set_color(PRIMARY_COLOR).scale(1.1),
            run_time=1.5,
            rate_func=rate_functions.ease_in_cubic
        )

        # Internal "Awareness" simulation (brief highlight)
        self.play(Indicate(transformer_box, color=PRIMARY_COLOR, scale_factor=1.02))
        self.wait(0.3)

        # Action: They emerge as 5 glowing yellow (rendered here as PRIMARY pink-red) vectors
        # Note: Following your color palette, context-aware = PRIMARY_COLOR glow
        self.play(
            FadeIn(output_group, shift=RIGHT),
            mechanism_label.animate.set_color(GRAY_B).scale(1/1.1),
            run_time=1.5,
            rate_func=rate_functions.ease_out_cubic
        )

        # Final Polish: Context Label
        context_aware_text = Text("Now 'Context-Aware'", font_size=20, color=PRIMARY_COLOR)
        context_aware_text.next_to(output_group, UP, buff=0.5)
        self.play(Write(context_aware_text))

        self.wait(3)

from manim import *

# --- Color Palette (White Background Theme) ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Context-Aware Glow)
STATIC_VECTOR_COLOR = "#e26fa2"     # Blue (Initial Static Vectors)
TRANSFORMER_BOX_COLOR = "#e5e7eb" # Light Grey for the box on white bg
TEXT_COLOR = BLACK             # Black text for white background
BG_COLOR = WHITE               # Clean White Background

class TransformerBlockIntroWhite(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- 1. HEADER ---
        title = Text("", font_size=28, color=TEXT_COLOR, weight=NORMAL)
        title.to_edge(UP, buff=0.5)

        # --- 2. THE TRANSFORMER BLOCK ---
        transformer_box = RoundedRectangle(
            corner_radius=0.2, height=4.5, width=5.5, # Slightly taller for internal text spacing
            fill_color=TRANSFORMER_BOX_COLOR, fill_opacity=0.5,
            stroke_color=GRAY, stroke_width=2
        )
        box_label = Text("Transformer Block", font_size=22, color=GRAY_D).next_to(transformer_box, UP, buff=0.2)
        
        # Mathematical Operation Symbol inside block
        math_op = MathTex(
            "Z = \\text{Attention}(X)", 
            font_size=32, 
            color=PRIMARY_COLOR
        ).move_to(transformer_box.get_center())
        
        transformer_group = VGroup(transformer_box, box_label, math_op).shift(DOWN * 0.2)

        # --- 3. SETUP INPUT/OUTPUT DATA ---
        word_list = ["The", "cat", "sat", "on", "the"]
        
        def create_vector_stack(color, opacity=1.0):
            return VGroup(*[
                Rectangle(height=1.0, width=0.25, fill_color=color, fill_opacity=opacity, stroke_width=1)
                for _ in range(5)
            ]).arrange(RIGHT, buff=0.5)

        # --- INPUT SIDE (Left) ---
        input_vectors = create_vector_stack(STATIC_VECTOR_COLOR)
        
        # Math Labels (x_i)
        input_math_labels = VGroup(*[
            MathTex(f"x_{i+1}", font_size=20, color=STATIC_VECTOR_COLOR)
            for i in range(5)
        ])
        for i, label in enumerate(input_math_labels):
            label.next_to(input_vectors[i], DOWN, buff=0.15)
            
        # NEW: Word Labels below math labels
        input_word_labels = VGroup(*[
            Text(word, font_size=16, color=STATIC_VECTOR_COLOR)
            for word in word_list
        ])
        for i, label in enumerate(input_word_labels):
            label.next_to(input_math_labels[i], DOWN, buff=0.15)
        
        # Grouping all input elements
        input_group = VGroup(input_vectors, input_math_labels, input_word_labels).to_edge(LEFT, buff=0.8)

        # --- OUTPUT SIDE (Right) ---
        output_vectors = create_vector_stack(PRIMARY_COLOR)
        glow_vectors = output_vectors.copy().set_stroke(PRIMARY_COLOR, width=6, opacity=0.3)
        
        # Math Labels (y_i)
        output_math_labels = VGroup(*[
            MathTex(f"y_{i+1}", font_size=20, color=PRIMARY_COLOR)
            for i in range(5)
        ])
        for i, label in enumerate(output_math_labels):
            label.next_to(output_vectors[i], DOWN, buff=0.15)

        # NEW: Word Labels below math labels
        output_word_labels = VGroup(*[
            Text(word, font_size=16, color=PRIMARY_COLOR)
            for word in word_list
        ])
        for i, label in enumerate(output_word_labels):
            label.next_to(output_math_labels[i], DOWN, buff=0.15)

        # NEW: "context-aware." descriptor
        context_sub_label = Text("Context-aware", font_size=20, color=PRIMARY_COLOR, slant=ITALIC)
        context_sub_label.next_to(output_word_labels, DOWN, buff=0.3)
            
        # Grouping all output elements
        output_group = VGroup(output_vectors, glow_vectors, output_math_labels, output_word_labels, context_sub_label).to_edge(RIGHT, buff=0.8)

        # --- 4. ANIMATION SEQUENCE ---
        self.play(FadeIn(title, shift=DOWN), FadeIn(transformer_group, shift=UP))
        self.wait(0.5)

        # Entry: vectors and labels appear
        self.play(
            Create(input_vectors), 
            Write(input_math_labels),
            Write(input_word_labels),
            run_time=1.2
        )
        self.wait(0.5)

        # Transformation: Moving into the block
        self.play(
            input_group.animate.move_to(transformer_box.get_center()).scale(0.2).set_opacity(0),
            math_op.animate.scale(1.2).set_color(TEXT_COLOR), # Turn black momentarily
            run_time=1.5,
            rate_func=rate_functions.ease_in_quad
        )

        # Computation Pulse
        self.play(Indicate(math_op, color=PRIMARY_COLOR), run_time=0.8)
        self.wait(0.2)

        # Emergence: Context-Aware result
        # The whole output group (vectors, math labels, words, context label) fades in together
        self.play(
            FadeIn(output_group, shift=RIGHT, lag_ratio=0.05),
            math_op.animate.scale(1/1.2).set_color(PRIMARY_COLOR),
            run_time=1.8,
            rate_func=rate_functions.ease_out_quad
        )

        # Final Mathematical Context Header
        context_desc = MathTex(
            "Y = f_{context}(X)", 
            font_size=24, 
            color=PRIMARY_COLOR
        ).next_to(output_group, UP, buff=0.5)
        self.play(Write(context_desc))

        self.wait(3)

from manim import *

# --- Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Relevance)
TEXT_COLOR = BLACK             # Black text for white background
BG_COLOR = WHITE               # Clean White Background

class MechanismOfAttention(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- 1. HEADER ---
        title = Text("How Attention Works?", font_size=28, color=BLACK, weight=NORMAL)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # --- 2. SENTENCE SETUP ---
        words_list = ["The", "cat", "sat", "on", "the"]
        sentence_group = VGroup(*[Text(w, font_size=36, color=BLACK) for w in words_list])
        # Wide separation for clarity and to accommodate labels
        sentence_group.arrange(RIGHT, buff=1.3)
        sentence_group.shift(DOWN * 0.5)

        # Reference specific words
        cat = sentence_group[1]
        sat = sentence_group[2]
        the_end = sentence_group[4]

        # Highlight for the query word "sat"
        sat_highlight = SurroundingRectangle(sat, color=PRIMARY_COLOR, buff=0.1, fill_opacity=0.1, stroke_width=2)

        # --- 3. ATTENTION ARROWS (Both Thin Style) ---

        # HIGH RELEVANCE: sat -> cat (THIN, CURVING FROM TOP)
        arrow_to_cat = CurvedArrow(
            sat.get_top() + UP * 0.1,
            cat.get_top() + UP * 0.1,
            angle=PI / 3,
            color=PRIMARY_COLOR
        ).set_stroke(width=2, opacity=1.0) # Thin weight, full opacity
        
        # Refining the top arrow tip to match the thin style
        arrow_to_cat.tip.set_stroke(width=0)
        arrow_to_cat.tip.set_fill(opacity=1.0)
        arrow_to_cat.tip.scale(0.6)

        label_cat = Text("High Relevance", font_size=16, color=PRIMARY_COLOR)
        label_cat.next_to(arrow_to_cat, UP, buff=0.2)

        # LOW RELEVANCE: sat -> the (THIN, CURVING FROM BOTTOM)
        arrow_to_the = CurvedArrow(
            sat.get_bottom() + DOWN * 0.1,
            the_end.get_bottom() + DOWN * 0.1,
            angle=PI / 4,
            color=PRIMARY_COLOR
        ).set_stroke(width=2, opacity=0.4) # Thin weight, faded opacity
        
        # Refining the bottom arrow tip
        arrow_to_the.tip.set_stroke(width=0)
        arrow_to_the.tip.set_fill(opacity=0.4)
        arrow_to_the.tip.scale(0.6)

        label_the = Text("Low Relevance", font_size=14, color=PRIMARY_COLOR).set_opacity(0.5)
        label_the.next_to(arrow_to_the, DOWN, buff=0.2)

        # --- 4. ANIMATION SEQUENCE ---
        self.play(Write(sentence_group), run_time=1.5)
        self.wait(0.5)

        # Action: "sat" lights up
        self.play(
            sat.animate.set_color(PRIMARY_COLOR),
            Create(sat_highlight),
            run_time=0.8
        )
        self.wait(0.2)

        # Action: Both Thin Arrows shoot out
        self.play(
            Create(arrow_to_cat),
            Create(arrow_to_the),
            run_time=1.5
        )

        # Action: Labels appear
        self.play(
            FadeIn(label_cat, shift=UP),
            FadeIn(label_the, shift=DOWN),
            run_time=1
        )

        self.wait(3)

from manim import *

# --- Updated Color Palette for White Background ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = "#ffffff" # Very Light Pink (for backgrounds of boxes)
ACCENT_COLOR = "#be185d"    # Darker shade for contrast
TEXT_COLOR = "#1f2937"      # Dark Grey/Black for prose
WHITE_BG = "#ffffff"        # Pure White Background

class SearchAnalogyWhite(Scene):
    def construct(self):
        # Set the background color to white
        self.camera.background_color = WHITE_BG

        # 1. Title Setup
        # Requirement: Title BLACK, NOT bold
        title_text = Text(
            "", 
            color=BLACK, 
            weight=NORMAL, 
            font_size=36
        ).to_edge(UP, buff=0.5)
        

        self.add(title_text)

        # 2. Defining the Words
        sat_label = Text("Sat", color=PRIMARY_COLOR, font_size=44).shift(LEFT * 3.5 + UP * 1)
        cat_label = Text("Cat", color=PRIMARY_COLOR, font_size=44).shift(RIGHT * 3.5 + UP * 1)

        self.play(Write(sat_label), Write(cat_label))

        # 3. The Query (Search Bar for "Sat")
        # Using a light pink fill to make the box pop on white
        query_box = RoundedRectangle(
            corner_radius=0.1, height=1.3, width=4.2, 
            color=PRIMARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=0.3
        ).next_to(sat_label, DOWN, buff=0.6)
        
        query_header = Text("QUERY", color=ACCENT_COLOR, font_size=18).next_to(query_box, UP, buff=0.1)
        query_content = Text('"Who is my subject?"', color=TEXT_COLOR, font_size=24).move_to(query_box.get_center())

        # 4. The Key (Tag for "Cat")
        key_tag = RoundedRectangle(
            corner_radius=0.5, height=1.3, width=4.2, 
            color=ACCENT_COLOR, fill_color=WHITE, fill_opacity=1
        ).next_to(cat_label, DOWN, buff=0.6)
        
        key_header = Text("KEY", color=PRIMARY_COLOR, font_size=18).next_to(key_tag, UP, buff=0.1)
        key_content = Text('"I am the subject."', color=TEXT_COLOR, font_size=24).move_to(key_tag.get_center())

        # 5. Animation Sequence
        self.play(
            Create(query_box), 
            FadeIn(query_header), 
            Write(query_content),
            run_time=1
        )
        self.wait(0.5)
        
        self.play(
            Create(key_tag), 
            FadeIn(key_header), 
            Write(key_content),
            run_time=1
        )

        # 6. The Match Process
        connection_line = DashedLine(
            query_box.get_right(), key_tag.get_left(), 
            color=PRIMARY_COLOR, buff=0.2
        )
        match_label = Text("MATCH FOUND", color=ACCENT_COLOR, font_size=20).next_to(connection_line, UP, buff=0.1)

        self.play(Create(connection_line), Write(match_label))
        self.play(Indicate(connection_line, color=PRIMARY_COLOR))

        # 7. The Value (Information Payload)
        # Using a solid PRIMARY_COLOR box with white text for high impact
        value_box = Rectangle(
            height=1.2, width=3.5, 
            fill_color=PRIMARY_COLOR, fill_opacity=1, 
            stroke_width=0
        ).shift(DOWN * 2.8)
        
        value_header = Text("VALUE (Information Shared)", color=ACCENT_COLOR, font_size=18).next_to(value_box, UP, buff=0.1)
        value_content = Text("Feline Features", color=WHITE, font_size=26).move_to(value_box.get_center())

        # Action: Show the result of the search
        self.play( 

            FadeIn(value_box, shift=UP),
            FadeIn(value_header),
            Write(value_content),
            run_time=1.5
        )
        
        # Final highlight on the 'meaning'
        self.play(value_box.animate.scale(1.1), rate_func=there_and_back)
        self.wait(2)

from manim import *

# --- Color Palette for White Background ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
ACCENT_COLOR = "#be185d"    # Darker shade
TEXT_COLOR = "#1f2937"      # Dark Grey/Black
WHITE_BG = "#ffffff"        # Background

class Scene11DotProduct(Scene):
    def construct(self):
        # Set background to white
        self.camera.background_color = WHITE_BG

        # 1. Title Setup (Black, Not Bold)
        title_text = Text(
            "", 
            color=BLACK, 
            weight=NORMAL, 
            font_size=32
        ).to_edge(UP, buff=0.5)
        self.add(title_text)

        # 2. Define Vectors
        # Query Vector ('sat')
        q_label = Text("Query ('sat')", color=TEXT_COLOR, font_size=24).shift(LEFT * 3 + UP * 2)
        q_vector = Matrix(
            [[2.5], [0.8], [3.1]],
            element_to_mobject_config={"color": TEXT_COLOR, "font_size": 30},
            bracket_config={"color": TEXT_COLOR}
        ).next_to(q_label, DOWN)
        
        # Key Vector ('cat')
        k_label = Text("Key ('cat')", color=TEXT_COLOR, font_size=24).shift(RIGHT * 3 + UP * 2)
        k_vector = Matrix(
            [[2.8], [0.5], [3.5]],
            element_to_mobject_config={"color": TEXT_COLOR, "font_size": 30},
            bracket_config={"color": TEXT_COLOR}
        ).next_to(k_label, DOWN)

        dot_symbol = MathTex(r"\cdot", color=PRIMARY_COLOR, font_size=80).move_to(ORIGIN)

        # 3. Resulting Equation
        # Fix: Removed 'weight' and added \mathbf for bolding math
        equation_start = MathTex(
            r"q_{\text{sat}} \cdot k_{\text{cat}} =", 
            color=TEXT_COLOR, 
            font_size=48
        ).shift(LEFT * 1.5)
        
        # Applying colors to the math components
        equation_start[0][0:4].set_color(PRIMARY_COLOR) # q_sat
        equation_start[0][5:9].set_color(ACCENT_COLOR)  # k_cat

        # Result: Using \mathbf{} inside MathTex for the bold look
        result_score = MathTex(r"\mathbf{42.0}", color=PRIMARY_COLOR, font_size=72).next_to(equation_start, RIGHT)
        
        meaning_label = Text(
            "High Score = High Relevance\n(The model 'realizes' the connection)", 
            color=ACCENT_COLOR, 
            font_size=20,
            line_spacing=1.2
        ).next_to(result_score, DOWN, buff=0.8)

        # --- Animation Sequence ---
        self.play(FadeIn(VGroup(q_label, q_vector, k_label, k_vector), shift=UP*0.3))
        self.wait(0.5)

        self.play(
            q_vector.animate.next_to(dot_symbol, LEFT),
            k_vector.animate.next_to(dot_symbol, RIGHT),
            Write(dot_symbol)
        )
        self.wait(1)

        # Clean transition to the final math expression
        self.play(
            ReplacementTransform(VGroup(q_vector, dot_symbol, k_vector), equation_start),
            FadeOut(q_label), FadeOut(k_label),
            run_time=1.5
        )
        
        self.play(Write(result_score), run_time=1)
        self.play(Indicate(result_score, color=PRIMARY_COLOR), FadeIn(meaning_label, shift=UP*0.2))
        self.wait(2)

from manim import *

# --- Configuration & Color Palette ---
# PRIMARY_COLOR = "#db2777" (Pinkish-Red)
# ACCENT_COLOR = "#be185d" (Darker shade)
# TEXT_COLOR = "#1f2937" (Dark Grey/Black)
# WHITE_BG = "#ffffff" (Background)

class Scene09Trinity(Scene):
    def construct(self):
        # Set background to white
        self.camera.background_color = "#ffffff"
        
        # Define Colors
        PRIMARY_COLOR = "#db2777"
        ACCENT_COLOR = "#be185d"
        TEXT_COLOR = "#1f2937"
        
        # 1. Title (Requirement: BLACK, NOT bold)
        title = Text(
            "", 
            color=BLACK, weight=NORMAL, font_size=32
        ).to_edge(UP, buff=0.5)
        self.add(title)

        # 2. Input Vector x_sat
        x_sat_label = MathTex(r"x_{\text{sat}}", color=TEXT_COLOR, font_size=36)
        x_sat_vec = Matrix(
            [[1.1], [2.4], [-0.5]], 
            element_to_mobject_config={"color": TEXT_COLOR},
            bracket_config={"color": TEXT_COLOR}
        ).next_to(x_sat_label, DOWN)
        x_group = VGroup(x_sat_label, x_sat_vec).shift(LEFT * 5 + UP * 0.5)

        # 3. The Learned Weight Matrices (W_Q, W_K, W_V)
        matrix_style = {
            "element_to_mobject_config": {"color": PRIMARY_COLOR, "font_size": 22},
            "bracket_config": {"color": PRIMARY_COLOR},
            "h_buff": 0.7, "v_buff": 0.5
        }
        
        W_Q = Matrix([[0.1, 0.5, 0.2], [0.3, 0.1, 0.8], [0.9, 0.4, 0.2]], **matrix_style)
        W_K = Matrix([[0.4, 0.2, 0.9], [0.5, 0.8, 0.1], [0.2, 0.3, 0.4]], **matrix_style)
        W_V = Matrix([[0.1, 0.1, 0.1], [0.5, 0.5, 0.5], [0.9, 0.9, 0.9]], **matrix_style)

        W_Q_lbl = MathTex(r"W_Q", color=PRIMARY_COLOR).next_to(W_Q, UP)
        W_K_lbl = MathTex(r"W_K", color=PRIMARY_COLOR).next_to(W_K, UP)
        W_V_lbl = MathTex(r"W_V", color=PRIMARY_COLOR).next_to(W_V, UP)

        w_q_group = VGroup(W_Q_lbl, W_Q)
        w_k_group = VGroup(W_K_lbl, W_K)
        w_v_group = VGroup(W_V_lbl, W_V)

        matrices = VGroup(w_q_group, w_k_group, w_v_group).arrange(RIGHT, buff=0.6).shift(RIGHT * 1.5)

        # 4. Resulting Query Vector q_sat
        q_sat_label = MathTex(r"q_{\text{sat}}", color=ACCENT_COLOR, font_size=36)
        q_sat_vec = Matrix(
            [[0.9], [1.8], [1.2]], 
            element_to_mobject_config={"color": ACCENT_COLOR},
            bracket_config={"color": ACCENT_COLOR}
        ).next_to(q_sat_label, DOWN)
        q_group = VGroup(q_sat_label, q_sat_vec)

        # Semantic Role Text (Clarifying the "Query" as a projection)
        semantic_info = Text(
            'The Query:\n"I am a verb, who is my subject?"', 
            color=ACCENT_COLOR, font_size=18, line_spacing=1.2, weight=NORMAL
        )

        # --- Animation Sequence ---

        # Step 1: Introduction of the "Trinity"
        self.play(FadeIn(x_group, shift=RIGHT))
        self.play(LaggedStart(FadeIn(w_q_group), FadeIn(w_k_group), FadeIn(w_v_group), lag_ratio=0.2))
        self.wait(1)

        # Step 2: Focus Phase - W_K and W_V fade away completely
        # Moving x_sat and W_Q to the center for multiplication
        dot = MathTex(r"\cdot", color=TEXT_COLOR, font_size=48).move_to(LEFT * 1.8)
        
        self.play(
            FadeOut(w_k_group),
            FadeOut(w_v_group),
            w_q_group.animate.scale(1.1).move_to(RIGHT * 0.8),
            x_group.animate.scale(1.1).next_to(dot, LEFT, buff=0.3),
            Write(dot),
            run_time=1.5
        )

        # Step 3: Transformation to q_sat
        arrow = Arrow(RIGHT * 2.5, RIGHT * 4.2, color=TEXT_COLOR)
        q_group.next_to(arrow, RIGHT, buff=0.3)
        semantic_info.next_to(q_group, DOWN, buff=0.8)

        self.play(GrowArrow(arrow))
        
        # Mathematically honest transition: q = x * W
        self.play(
            ReplacementTransform(x_group.copy(), q_group),
            ReplacementTransform(w_q_group.copy(), q_group),
            run_time=2
        )
        
        self.play(Write(semantic_info))
        self.wait(2)

        # Step 4: Final explanation note
        note = Text(
            "q_sat is a direction in space that determines\nwhich other tokens will matter.",
            color=TEXT_COLOR, font_size=16, weight=NORMAL
        ).to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(note))
        self.wait(3)

