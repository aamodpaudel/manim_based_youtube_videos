from manim import *
import numpy as np

# --- Configuration & Color Palette ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = "#fce7f3" # Very Light Pink
ACCENT_COLOR = "#be185d"    # Darker shade
TEXT_COLOR = "#1f2937"      # Dark Grey/Black
GRID_COLOR = "#e5e7eb"      # Light grey
WHITE_BG = "#ffffff"        # Background

class AttentionCell(VGroup):
    """
    A custom Mobject representing a single cell in the Attention Matrix.
    Uses explicit z_index to prevent text disappearing during highlights.
    """
    def __init__(self, value, size=1.2, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        
        # 1. Base Square (Layer 0)
        self.rect = Square(
            side_length=size, 
            fill_color=WHITE_BG, 
            fill_opacity=1, 
            stroke_color=GRID_COLOR, 
            stroke_width=2
        ).set_z_index(0)
        
        # 2. Highlight Layer (Layer 1 - Between rect and text)
        self.highlight_box = Square(
            side_length=size, 
            fill_color=PRIMARY_COLOR, 
            fill_opacity=0, 
            stroke_width=0
        ).move_to(self.rect).set_z_index(1)
        
        # 3. Text Value (Layer 2 - Always on top)
        self.label = Text(
            str(value), 
            color=TEXT_COLOR, 
            font_size=24,
            weight=NORMAL
        ).move_to(self.rect).set_z_index(2)
        
        self.add(self.rect, self.highlight_box, self.label)

    def get_highlight_animation(self, opacity=0.8, color=PRIMARY_COLOR):
        """Returns the animation to fill the cell background."""
        return self.highlight_box.animate.set_fill(color, opacity=opacity)

    def get_text_highlight(self, color=WHITE):
        """Returns animation to change text color; z-index ensures visibility."""
        return self.label.animate.set_color(color)

class Scene12AttentionMatrix(Scene):
    def construct(self):
        # --- Stage 1: Initialization ---
        self.camera.background_color = WHITE_BG
        
        # 1.1 Title Setup (Black, Not Bold)
        title = Text(
            "", 
            color=BLACK, 
            weight=NORMAL, 
            font_size=36
        ).to_edge(UP, buff=0.5)
        
        self.add(title)

        # 1.2 Data Definitions
        words = ["The", "cat", "sat", "on", "the"]
        n = len(words)
        
        # Matrix values representing attention scores
        scores = [
            [12.1, 4.2, 1.1, 5.5, 9.8],
            [3.2, 28.5, 14.2, 2.1, 3.8],
            [1.5, 42.0, 22.1, 11.2, 1.9],  # The 'sat' row
            [4.1, 2.5, 15.6, 18.2, 5.3],
            [8.9, 3.8, 1.2, 6.7, 10.5]
        ]

        # --- Stage 2: Building the UI ---
        
        # 2.1 The Grid
        cell_size = 1.2
        grid = VGroup()
        matrix_cells = [] 

        for i in range(n):
            row_cells = []
            for j in range(n):
                cell = AttentionCell(value=f"{scores[i][j]:.1f}", size=cell_size)
                # Centering logic with offset for left-side header
                cell.move_to(RIGHT * 0.5 + DOWN * 0.5 + RIGHT * (j - 2) * cell_size + DOWN * (i - 2) * cell_size)
                row_cells.append(cell)
                grid.add(cell)
            matrix_cells.append(row_cells)

        # 2.2 Row Labels (Queries)
        query_labels = VGroup()
        for i, word in enumerate(words):
            lbl = Text(word, color=TEXT_COLOR, font_size=24)
            lbl.next_to(matrix_cells[i][0], LEFT, buff=0.8) 
            query_labels.add(lbl)
            
        # Spacing: Far to the left to avoid touching the table
        query_header = Text("Queries (Q)", color=PRIMARY_COLOR, font_size=22)\
            .next_to(query_labels, LEFT, buff=1.0)

        # 2.3 Column Labels (Keys)
        key_labels = VGroup()
        for j, word in enumerate(words):
            lbl = Text(word, color=TEXT_COLOR, font_size=24)
            lbl.next_to(matrix_cells[0][j], UP, buff=0.6)
            key_labels.add(lbl)
            
        # Spacing: Far to the right to maintain professional gap
        key_header = Text("Keys (K)", color=ACCENT_COLOR, font_size=22)\
            .next_to(key_labels, RIGHT, buff=1.2).align_to(key_labels, UP)

        # --- Stage 3: Animation Sequence ---

        # 3.1 Reveal Headers and Labels
        self.play(
            FadeIn(query_header, shift=RIGHT * 0.3),
            FadeIn(key_header, shift=LEFT * 0.3),
            run_time=1
        )
        
        self.play(
            LaggedStart(*[FadeIn(q, shift=RIGHT * 0.2) for q in query_labels], lag_ratio=0.1),
            LaggedStart(*[FadeIn(k, shift=DOWN * 0.2) for k in key_labels], lag_ratio=0.1),
            run_time=1.5
        )

        # 3.2 Create Grid and Reveal Scores
        self.play(
            LaggedStart(*[Create(c.rect) for row in matrix_cells for c in row], lag_ratio=0.01),
            run_time=1.5
        )
        
        self.play(
            LaggedStart(*[Write(c.label) for row in matrix_cells for c in row], lag_ratio=0.01),
            run_time=1.5
        )
        self.wait(1)

        # 3.3 The Intersection Highlight
        # target: "sat" (Query index 2) x "cat" (Key index 1)
        target_cell = matrix_cells[2][1]
        target_query = query_labels[2]
        target_key = key_labels[1]

        # Visual Guides
        h_line = Line(target_query.get_right(), target_cell.get_left(), color=PRIMARY_COLOR, stroke_width=2)
        v_line = Line(target_key.get_bottom(), target_cell.get_top(), color=ACCENT_COLOR, stroke_width=2)

        self.play(
            Create(h_line), 
            Create(v_line),
            target_query.animate.set_color(PRIMARY_COLOR).scale(1.1),
            target_key.animate.set_color(ACCENT_COLOR).scale(1.1),
            run_time=1
        )

        # FIX: Explicit z_index in AttentionCell class ensures '42.0' turns WHITE and stays visible
        self.play(
            target_cell.get_highlight_animation(opacity=0.9, color=PRIMARY_COLOR),
            target_cell.get_text_highlight(color=WHITE),
            run_time=1
        )
        
        # 3.4 Cleanup and Final Pause
        self.play(FadeOut(h_line), FadeOut(v_line))
        self.wait(3)

from manim import *
import numpy as np

# --- Configuration & Color Palette ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
ACCENT_COLOR = "#be185d"    # Darker shade
TEXT_COLOR = "#1f2937"      # Dark Grey/Black
WHITE_BG = "#ffffff"        # Background
GRID_COLOR = "#e5e7eb"      # Light grey

class SoftmaxCell(VGroup):
    def __init__(self, raw_val, softmax_val, size=1.1, **kwargs):
        super().__init__(**kwargs)
        self.raw_val = raw_val
        self.softmax_val = softmax_val
        
        # 1. Base Layer
        self.bg = Square(
            side_length=size, fill_color=WHITE_BG, fill_opacity=1, 
            stroke_color=GRID_COLOR, stroke_width=2
        ).set_z_index(0)
        
        # 2. Highlight Layer
        self.highlight = Square(
            side_length=size, fill_color=PRIMARY_COLOR, fill_opacity=0, 
            stroke_width=0
        ).move_to(self.bg).set_z_index(1)
        
        # 3. Raw Text
        self.raw_text = Text(f"{raw_val:.1f}", color=TEXT_COLOR, font_size=22).set_z_index(2)
        
        # 4. Softmax Text - Now using real calculated percentages
        perc = int(round(softmax_val * 100))
        self.soft_text = Text(f"{perc}%", color=TEXT_COLOR, font_size=22).set_z_index(2)
        self.soft_text.set_opacity(0)
        
        self.add(self.bg, self.highlight, self.raw_text, self.soft_text)
        self.raw_text.move_to(self.bg.get_center())
        self.soft_text.move_to(self.bg.get_center())

    def update_to_softmax(self, is_focus=False):
        # Dynamically color based on probability weight
        target_color = WHITE if is_focus else (PRIMARY_COLOR if self.softmax_val > 0.1 else TEXT_COLOR)
        
        anims = [
            self.raw_text.animate.set_opacity(0).scale(0.5),
            self.soft_text.animate.set_opacity(1).set_color(target_color),
        ]
        if is_focus:
            anims.append(self.highlight.animate.set_fill(opacity=0.9))
        elif self.softmax_val > 0.1:
            # Subtle highlight for secondary attention
            anims.append(self.highlight.animate.set_fill(color=PRIMARY_COLOR, opacity=0.2))
        
        return AnimationGroup(*anims)

class Scene13SoftmaxUpdated(Scene):
    def construct(self):
        self.camera.background_color = WHITE_BG
        
        # 1. Title (Black, Not Bold)
        title = Text("", color=BLACK, weight=NORMAL, font_size=32).to_edge(UP, buff=0.4)
        self.add(title)

        # 2. Data Preparation - Using smaller numbers for visual distribution
        words = ["The", "cat", "sat", "on", "the"]
        n = len(words)
        
        # Adjusted scores so 'sat' (index 2) likes 'cat' (index 1) but also sees 'on' (index 3)
        raw_data = np.array([
            [2.1, 1.2, 0.5, 0.8, 1.9],
            [0.8, 3.5, 2.1, 0.4, 0.6],
            [1.1, 4.2, 2.8, 1.5, 0.9], # 'sat' row: 4.2 is high, but 2.8 is also relevant
            [0.6, 0.5, 2.4, 3.1, 1.2],
            [1.8, 1.1, 0.4, 0.9, 2.0]
        ])

        def sm(row):
            e = np.exp(row - np.max(row))
            return e / e.sum()
        softmax_data = np.apply_along_axis(sm, 1, raw_data)

        # 3. Grid Construction
        cell_size = 1.1
        grid_cells = []
        all_cells = VGroup()
        
        for i in range(n):
            row = []
            for j in range(n):
                c = SoftmaxCell(raw_data[i][j], softmax_data[i][j], size=cell_size)
                # Spacing to ensure no overlap
                c.move_to(DOWN * 0.8 + RIGHT * (j-2) * cell_size + DOWN * (i-1.5) * cell_size)
                row.append(c)
                all_cells.add(c)
            grid_cells.append(row)

        q_labels = VGroup(*[Text(w, font_size=20, color=TEXT_COLOR).next_to(grid_cells[i][0], LEFT, buff=0.8) for i, w in enumerate(words)])
        k_labels = VGroup(*[Text(w, font_size=20, color=TEXT_COLOR).next_to(grid_cells[0][j], UP, buff=0.4) for j, w in enumerate(words)])
        
        q_header = Text("Queries", color=PRIMARY_COLOR, font_size=18).next_to(q_labels, LEFT, buff=1.0)
        k_header = Text("Keys", color=ACCENT_COLOR, font_size=18).next_to(k_labels, UP, buff=0.6)

        formula = MathTex(r"\sigma(x)_i = \frac{e^{x_i}}{\sum e^{x_j}}", color=PRIMARY_COLOR, font_size=28)

        # --- Animation ---
        self.play(FadeIn(q_header), FadeIn(k_header), Write(q_labels), Write(k_labels))
        self.play(LaggedStart(*[AnimationGroup(FadeIn(c.bg), Write(c.raw_text)) for c in all_cells], lag_ratio=0.01))
        self.wait(1)

        # 1. Highlight 'sat' row
        sat_row = VGroup(*grid_cells[2])
        focus_box = SurroundingRectangle(sat_row, color=PRIMARY_COLOR, buff=0.1)
        self.play(Create(focus_box))

        # 2. Softmax Formula Entrance (Right side as requested)
        formula.next_to(sat_row, RIGHT, buff=0.8)
        self.play(FadeIn(formula, shift=LEFT * 0.4))

        # 3. Transition Scores
        self.play(
            AnimationGroup(
                *[grid_cells[2][j].update_to_softmax(is_focus=(j==1)) for j in range(n)],
                lag_ratio=0.1
            ),
            run_time=2
        )

        # 4. Sum Label
        sum_label = Text("Scores now sum to 100%", color=PRIMARY_COLOR, font_size=18).next_to(formula, DOWN, buff=0.3)
        self.play(Write(sum_label))
        self.wait(1)

        # 5. Rest of the table
        rest = [grid_cells[i][j] for i in range(n) for j in range(n) if i != 2]
        self.play(
            AnimationGroup(*[c.update_to_softmax() for c in rest], lag_ratio=0.01),
            FadeOut(focus_box),
            run_time=2
        )
        self.wait(2)

from manim import *

# --- Configuration & Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Theme color)
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink (Accents)
ACCENT_COLOR = "#be185d"       # Darker shade for emphasis
TEXT_COLOR = "#1f2937"         # Dark Grey for high contrast
WHITE_BG = "#ffffff"           # Background
CONTEXT_TEAL = "#430425"       # Final state color

class Scene14WeightedSum(Scene):
    def construct(self):
        self.camera.background_color = WHITE_BG

        # 1. Title Setup (Requirement: BLACK, NOT bold)
        title = Text(
            "", 
            color=BLACK, weight=NORMAL, font_size=36
        ).to_edge(UP, buff=0.5)
        self.add(title)

        # 2. Define Vector Objects
        # Left side: The Query word "sat"
        sat_rect = Rectangle(
            height=3.5, width=1.1, 
            fill_color=PRIMARY_COLOR, fill_opacity=0.1, 
            stroke_color=PRIMARY_COLOR, stroke_width=2
        ).shift(LEFT * 3.5 + DOWN * 0.5)
        sat_label = Text("Original 'sat'", color=TEXT_COLOR, font_size=20).next_to(sat_rect, DOWN, buff=0.5)

        # Right side: The Key word "cat" (The Information Source)
        cat_rect = Rectangle(
            height=3.5, width=1.1, 
            fill_color=ACCENT_COLOR, fill_opacity=1, 
            stroke_width=0
        ).shift(RIGHT * 3.5 + DOWN * 0.5)
        cat_label = Text("Value ('feline')", color=TEXT_COLOR, font_size=20).next_to(cat_rect, DOWN, buff=0.5)
        cat_desc = Text("[Contextual Info]", color=ACCENT_COLOR, font_size=16).next_to(cat_label, DOWN, buff=0.2)

        # 3. The 80% Weight Badge
        weight_box = RoundedRectangle(
            corner_radius=0.1, height=0.7, width=2.4, 
            color=PRIMARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=1
        ).next_to(cat_rect, UP, buff=0.5)
        weight_text = Text("80% Attention", color=PRIMARY_COLOR, font_size=20, weight=BOLD).move_to(weight_box)

        # --- Animation ---
        self.play(Create(sat_rect), Write(sat_label))
        self.play(FadeIn(cat_rect, shift=DOWN*0.3), Write(cat_label), FadeIn(cat_desc))
        self.play(Create(weight_box), Write(weight_text))
        self.wait(1)

        # 4. Action: The Information Blending
        # We create a copy that represents the 80% of "Cat" information being used
        blend_rect = cat_rect.copy().set_z_index(5)
        
        self.play(
            blend_rect.animate.stretch_to_fit_height(3.5 * 0.8).move_to(sat_rect.get_bottom(), aligned_edge=DOWN),
            run_time=2,
            rate_func=bezier([0, 0, 1, 1])
        )

        # 5. Final State: Transformation to Teal
        updated_sat = Rectangle(
            height=3.5, width=1.1, 
            fill_color=CONTEXT_TEAL, fill_opacity=1, 
            stroke_width=0
        ).move_to(sat_rect.get_center()).set_z_index(6)
        
        updated_label = Text("Contextualized 'sat'", color=CONTEXT_TEAL, font_size=20).next_to(updated_sat, DOWN, buff=0.5)
        updated_info = Text("(Sitting + Feline)", color=TEXT_COLOR, font_size=16).next_to(updated_label, DOWN, buff=0.2)

        self.play(
            ReplacementTransform(VGroup(sat_rect, blend_rect), updated_sat),
            ReplacementTransform(sat_label, updated_label),
            FadeOut(VGroup(cat_rect, cat_label, cat_desc, weight_box, weight_text)),
            Write(updated_info),
            run_time=1.5
        )
        self.play(Indicate(updated_sat, color=CONTEXT_TEAL))
        self.wait(3)

from manim import *

# --- Strictly Implemented Color Palette ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
ACCENT_COLOR = "#be185d"    # Darker shade
TEXT_COLOR = "#1f2937"      # Dark Grey/Black
WHITE_BG = "#ffffff"        # Background

class Scene15GoldenEquation(Scene):
    def construct(self):
        self.camera.background_color = WHITE_BG

        # 1. Title Setup (Requirement: BLACK, NOT bold)
        title = Text(
            "", 
            color=BLACK, 
            weight=NORMAL, 
            font_size=32
        ).to_edge(UP, buff=0.7)
        self.add(title)

        # 2. Equation Composition
        # We define the math components first
        lhs = MathTex(r"\text{Attention}(Q, K, V) =", color=TEXT_COLOR, font_size=44)
        
        softmax_part = MathTex(
            r"\text{softmax}\left( \frac{Q K^T}{\sqrt{d_k}} \right)",
            color=TEXT_COLOR, font_size=44
        )
        # Highlight the relevance calculation in pink
        softmax_part[0][8:11].set_color(PRIMARY_COLOR) 
        
        value_v = MathTex(r"V", color=ACCENT_COLOR, font_size=44)
        
        # Group only the math elements
        equation = VGroup(lhs, softmax_part, value_v).arrange(RIGHT, buff=0.3).move_to(ORIGIN)

        # 3. Create the Surrounding Box FIRST
        # We use a generous buff to give the math breathing room
        frame = SurroundingRectangle(
            equation, 
            color=PRIMARY_COLOR, 
            buff=0.6, 
            stroke_width=2
        )

        # 4. Position Labels relative to the FRAME (Bottom Edge)
        # This is the "Fix": Placing labels below the box, not the math.
        label_relevance = Text("Relevance Score", color=PRIMARY_COLOR, font_size=18)
        # Aligning to the center of the softmax math, but Y-position is based on the frame
        label_relevance.next_to(frame, DOWN, buff=0.5).align_to(softmax_part, LEFT)
        
        label_info = Text("Information Payload", color=ACCENT_COLOR, font_size=18)
        # Positioned below the frame to guarantee no overlap
        label_info.next_to(frame, DOWN, buff=0.5).align_to(value_v, LEFT)

        # --- Animation Sequence ---

        # Step 1: Write the equation
        self.play(Write(lhs), run_time=1)
        self.wait(0.2)
        
        # Step 2: Show the relevance/search part
        self.play(
            FadeIn(softmax_part, shift=UP*0.2),
            run_time=1
        )
        
        # Step 3: Show the information/content part
        self.play(
            FadeIn(value_v, shift=LEFT*0.2),
            run_time=1
        )
        self.wait(0.5)
        
        # Step 4: Create the frame and THEN the labels
        # Creating the frame first defines the boundaries
        self.play(Create(frame), run_time=1)
        
        # Now fade in labels below the frame
        self.play(
            FadeIn(label_relevance, shift=UP*0.2),
            FadeIn(label_info, shift=UP*0.2),
            run_time=1
        )
        
        # Final emphasis: Scale the whole visual unit together
        # We group them so they scale relative to the center of the whole visual
        final_group = VGroup(equation, frame, label_relevance, label_info)
        self.play(
            final_group.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=2
        )
        
        self.wait(3)


from manim import *

# --- Configuration & Color Palette ---
# Maintaining consistency with the established palette
WHITE_BG = "#ffffff"
TEXT_COLOR = "#1f2937"
GRID_COLOR = "#e5e7eb"

# Expanded palette for the 8 heads, starting with the primary theme color
HEAD_COLORS = [
    "#db2777", # Head 1 (Primary Pink)
    "#f97316", # Head 2 (Orange)
    "#eab308", # Head 3 (Gold)
    "#22c55e", # Head 4 (Green)
    "#14b8a6", # Head 5 (Teal - consistent with Scene 14 context)
    "#3b82f6", # Head 6 (Blue)
    "#6366f1", # Head 7 (Indigo)
    "#a855f7", # Head 8 (Purple)
]

class SimpleGrid(VGroup):
    """
    A simplified visual representation of an 5x5 attention grid for stacking.
    Doesn't need numbers, just the visual structure and color.
    """
    def __init__(self, color, side_len=0.8, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        for i in range(5):
            for j in range(5):
                # Create a semi-transparent filled square with a solid border
                sq = Square(
                    side_length=side_len,
                    fill_color=color,
                    fill_opacity=0.15,
                    stroke_color=color,
                    stroke_width=1.5
                )
                # Arrange in a 5x5 grid centered at ORIGIN
                sq.move_to(RIGHT * (j - 2) * side_len + DOWN * (i - 2) * side_len)
                self.add(sq)
        # Add a slightly thicker border around the whole grid for definition
        self.add(SurroundingRectangle(self, color=color, stroke_width=2, buff=0))

from manim import *

# --- Configuration & Consistent Palette ---
PRIMARY_COLOR = "#db2777"
SECONDARY_COLOR = "#fce7f3"
ACCENT_COLOR = "#be185d"
TEXT_COLOR = "#1f2937"
WHITE_BG = "#ffffff"

# Distinct colors for the 8 heads
HEAD_COLORS = [
    "#db2777", "#f97316", "#eab308", "#22c55e", 
    "#14b8a6", "#3b82f6", "#6366f1", "#a855f7"
]

class SimpleGrid(VGroup):
    def __init__(self, color, side_len=0.7, **kwargs):
        super().__init__(**kwargs)
        # Create a 5x5 grid structure
        grid = VGroup(*[
            Square(side_length=side_len, stroke_width=2, stroke_color=color, fill_color=color, fill_opacity=0.1) 
            for _ in range(25)
        ]).arrange_in_grid(5, 5, buff=0)
        self.add(grid)
        # Add border for definition
        self.add(SurroundingRectangle(grid, color=color, stroke_width=3, buff=0))

class Scene16MultiHeadAttention(Scene):
    def construct(self):
        self.camera.background_color = WHITE_BG

        # 1. Title Setup (Requirement: BLACK, NOT bold)
        title = Text(
            "",
            color=BLACK, weight=NORMAL, font_size=32
        ).to_edge(UP, buff=0.7)
        self.add(title)

        # 2. Initial State: Single Attention Head
        # Positioned to the left to leave space for right-side labels
        base_grid = SimpleGrid(color=HEAD_COLORS[0])
        base_grid.move_to(LEFT * 2.5 + DOWN * 0.5)
        
        base_label = Text("Single Attention Head", color=TEXT_COLOR, font_size=20).next_to(base_grid, DOWN, buff=0.5)

        self.play(Create(base_grid), Write(base_label))
        self.wait(1)

        # 3. The Transition: Fanning into 8 Heads
        # Create a diagonal stack where each layer is distinct
        heads = VGroup(*[SimpleGrid(color=c) for c in HEAD_COLORS])
        heads.move_to(base_grid.get_center())

        # Offset vector for the "pancake" effect
        stack_offset = UR * 0.25 

        self.play(
            FadeOut(base_label),
            ReplacementTransform(base_grid, heads[0]),
            LaggedStart(
                *[heads[i].animate.shift(stack_offset * i) for i in range(1, 8)],
                lag_ratio=0.1
            ),
            run_time=2.5
        )

        # 4. Non-Overlapping Labels (REVERSED ORDER logic)
        
        # Head 1: Placed BELOW the figure
        lbl1 = Text("Head 1: Grammar Rules", color=HEAD_COLORS[0], font_size=18)
        lbl1.next_to(heads[0], DOWN, buff=1.2).shift(RIGHT * 0.5)
        

        # Head 5: Placed NEXT to the figure (Center-Right)
        lbl5 = Text("Head 5: Semantic Nuance", color=HEAD_COLORS[4], font_size=18)
        lbl5.move_to(RIGHT * 3.5 + DOWN * 0.5)
       

        # Head 8: Placed towards the TOP (Right side)
        lbl8 = Text("Head 8: Long-range Context", color=HEAD_COLORS[7], font_size=18)
        lbl8.move_to(RIGHT * 3.5 + UP * 1.5)
        

        # 5. Final Animation Sequence
        # We reveal labels in order to show how different heads capture different nuances
        self.play(
            Write(lbl1),
            run_time=1
        )
        self.wait(0.3)
        
        self.play(
            Write(lbl5),
            run_time=1
        )
        self.wait(0.3)
        
        self.play(
            Write(lbl8),
            run_time=1
        )

        # Subtle emphasis pulse on the entire stack
        self.play(heads.animate.scale(1.05), rate_func=there_and_back, run_time=1.5)
        
        self.wait(3)


from manim import *

# --- Strictly Implemented Color Palette ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red (Theme color)
SECONDARY_COLOR = "#fce7f3" # Very Light Pink (Accents)
ACCENT_COLOR = "#be185d"    # Darker shade for nodes/highlights
TEXT_COLOR = "#1f2937"      # Dark Grey for high contrast
WHITE_BG = "#ffffff"        # Background
CONTEXT_TEAL = "#cf6a98"    # Context-aware vector color from Scene 14/16

class Scene17FFN(Scene):
    def construct(self):
        # 1. Setup Environment
        self.camera.background_color = WHITE_BG

        # 2. Title Setup (Requirement: BLACK, NOT bold)
        title = Text(
            "", 
            color=BLACK, 
            weight=NORMAL, 
            font_size=32
        ).to_edge(UP, buff=0.7)
        self.add(title)

        # 3. Define the Input Vector (Contextualized 'cat')
        # We start with the teal color established in the Attention phase
        input_vector = Rectangle(
            height=3, width=0.8, 
            fill_color=CONTEXT_TEAL, fill_opacity=1, 
            stroke_width=0
        ).shift(LEFT * 5 + DOWN * 0.5)
        
        input_label = Text("Context Vector", color=CONTEXT_TEAL, font_size=18).next_to(input_vector, DOWN, buff=0.4)
        input_sub = Text("('cat' + context)", color=TEXT_COLOR, font_size=14).next_to(input_label, DOWN, buff=0.1)
        
        input_group = VGroup(input_vector, input_label, input_sub)

        # 4. Define the FFN Box
        # A large professional container representing the 2-layer neural network
        ffn_box = RoundedRectangle(
            corner_radius=0.2, height=4, width=5, 
            color=PRIMARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=0.2,
            stroke_width=2
        ).shift(RIGHT * 0.5 + DOWN * 0.5)
        
        ffn_header = Text("Feed-Forward Network", color=PRIMARY_COLOR, font_size=24, weight=BOLD).next_to(ffn_box, UP, buff=0.5)

        # Visual representation of internal nodes (Minimalist)
        nodes_in = VGroup(*[Circle(radius=0.15, color=ACCENT_COLOR, fill_opacity=1) for _ in range(4)]).arrange(DOWN, buff=0.4)
        nodes_out = VGroup(*[Circle(radius=0.15, color=ACCENT_COLOR, fill_opacity=1) for _ in range(4)]).arrange(DOWN, buff=0.4)
        nodes_in.move_to(ffn_box.get_left() + RIGHT * 1)
        nodes_out.move_to(ffn_box.get_right() + LEFT * 1)
        
        # Connection lines inside FFN
        connections = VGroup()
        for start_node in nodes_in:
            for end_node in nodes_out:
                line = Line(start_node.get_center(), end_node.get_center(), stroke_width=1, color=PRIMARY_COLOR, stroke_opacity=0.3)
                connections.add(line)

        ffn_internal = VGroup(connections, nodes_in, nodes_out)
        ffn_group = VGroup(ffn_box, ffn_header, ffn_internal)

        # --- Animation Sequence ---

        # Step 1: Reveal Vector and FFN
        self.play(FadeIn(input_group, shift=RIGHT))
        self.play(Create(ffn_box), Write(ffn_header))
        self.play(LaggedStart(*[Create(n) for n in nodes_in + nodes_out], lag_ratio=0.1), Create(connections))
        self.wait(1)

        # Step 2: Vector Enters the FFN
        # Voiceover: "...it needs to 'think.' It enters the Feed-Forward Network."
        # We animate the vector moving into the box while labels fade
        self.play(
            input_vector.animate.move_to(ffn_box.get_center()).scale(0.8).set_opacity(0.5),
            FadeOut(input_label), 
            FadeOut(input_sub),
            run_time=2,
            rate_func=bezier([0, 0, 1, 1])
        )

        # Step 3: The "Thinking" Pulse
        # Nodes and connections pulse to show processing
        self.play(
            Indicate(ffn_internal, color=PRIMARY_COLOR, scale_factor=1.1),
            ffn_box.animate.set_fill(opacity=0.4),
            run_time=1.5
        )
        self.play(ffn_box.animate.set_fill(opacity=0.2))

        # Step 4: Emergence of the Processed Vector
        # The vector emerges on the right side, representing deeper abstraction
        processed_vector = input_vector.copy().set_opacity(1).scale(1.25).move_to(RIGHT * 5.5 + DOWN * 0.5)
        processed_vector.set_fill(color=ACCENT_COLOR) # Deepening the color
        
        processed_label = Text("Processed Vector", color=ACCENT_COLOR, font_size=18).next_to(processed_vector, DOWN, buff=0.4)
        processed_sub = Text("(Ready for Prediction)", color=TEXT_COLOR, font_size=14).next_to(processed_label, DOWN, buff=0.1)

        self.play(
            ReplacementTransform(input_vector, processed_vector),
            Write(processed_label),
            Write(processed_sub),
            run_time=2
        )

        self.wait(3)
    
from manim import *

# --- Strictly Implemented Color Palette ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = "#fce7f3" # Light Pink
ACCENT_COLOR = "#be185d"    # Darker shade
TEXT_COLOR = "#1f2937"      # Dark Grey
WHITE_BG = "#ffffff"        # Background
CONTEXT_TEAL = "#0d9488"    # Context-aware vector color

class Scene18FFNMath(Scene):
    def construct(self):
        self.camera.background_color = WHITE_BG

        # 1. Title Setup (Black, Normal Weight)
        title = Text(
            "Scene 18: FFN Mathematics", 
            color=BLACK, weight=NORMAL, font_size=32
        ).to_edge(UP, buff=0.7)
        self.add(title)

        # 2. The FFN Equation
        # Using LaTeX for formal math. W1 and W2 are colored to show "knowledge".
        equation = MathTex(
            r"W_2(\text{GELU}(W_1 x + b_1)) + b_2",
            color=TEXT_COLOR, font_size=42
        ).next_to(title, DOWN, buff=0.6)
        
        equation[0][0:2].set_color(ACCENT_COLOR)  # W2
        equation[0][7:9].set_color(PRIMARY_COLOR) # W1
        
        self.play(Write(equation))
        self.wait(1)

        # 3. Vector Representation (Input state)
        # The teal vector represents the context gathered from the attention layer
        vector = Rectangle(
            height=2, width=0.9, 
            fill_color=CONTEXT_TEAL, fill_opacity=1, 
            stroke_width=0
        ).move_to(DOWN * 1.5)
        
        dim_label = Text("d_model", color=TEXT_COLOR, font_size=18).next_to(vector, LEFT, buff=0.4)
        self.play(FadeIn(vector, shift=UP), Write(dim_label))

        # 4. Action: Expansion (First Linear Layer)
        # The vector expands to 49,152 dimensions (represented by stretching)
        expansion_label = Text("49,152 Dimensions", color=PRIMARY_COLOR, font_size=22, weight=BOLD)
        expansion_label.to_edge(RIGHT, buff=1.0).shift(UP * 0.5)
        
        expansion_desc = Text("(Massive Hidden Layer)", color=TEXT_COLOR, font_size=16)
        expansion_desc.next_to(expansion_label, DOWN, buff=0.2)

        # FIX: Using 'slow_into' instead of custom easing to avoid definition errors
        self.play(
            vector.animate.stretch_to_fit_height(6.5).set_fill(color=PRIMARY_COLOR),
            dim_label.animate.set_opacity(0),
            Write(expansion_label),
            Write(expansion_desc),
            run_time=2,
            rate_func=slow_into
        )
        
        # Pulse to represent processing
        self.play(Indicate(vector, color=ACCENT_COLOR), run_time=1)
        self.wait(1)

        # 5. Action: Compression (Second Linear Layer)
        # The vector returns to its original size, now "processed"
        final_dim_label = Text("Refined Vector", color=CONTEXT_TEAL, font_size=18).next_to(vector, LEFT, buff=0.4)

        # FIX: Using 'smooth' for the exit transition
        self.play(
            vector.animate.stretch_to_fit_height(2).set_fill(color=CONTEXT_TEAL),
            FadeOut(expansion_label),
            FadeOut(expansion_desc),
            FadeIn(final_dim_label),
            run_time=2,
            rate_func=smooth
        )

        # 6. Final Polish: The Knowledge Box
        # Large buff (0.6) to ensure the pink line doesn't overlap the sub-labels
        box = SurroundingRectangle(equation, color=PRIMARY_COLOR, buff=0.6, stroke_width=2)
        self.play(Create(box))
        
        self.wait(3)

from manim import *

# --- Strictly Implemented Color Palette ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = "#fce7f3" # Very Light Pink
ACCENT_COLOR = "#be185d"    # Darker shade
TEXT_COLOR = "#1f2937"      # Dark Grey
WHITE_BG = "#ffffff"        # Background
CONTEXT_TEAL = "#0d9488"    # Context-aware vector color

class Scene18FFNMath(Scene):
    def construct(self):
        self.camera.background_color = WHITE_BG

        # 1. Title Setup (Black, Normal Weight)
        title = Text(
            "FFN Mathematics", 
            color=BLACK, weight=NORMAL, font_size=32
        ).to_edge(UP, buff=0.7)
        self.add(title)

        # 2. The FFN Equation
        # We increase the buffer from the title to leave room for the SurroundingRectangle
        equation = MathTex(
            r"W_2(\text{GELU}(W_1 x + b_1)) + b_2",
            color=TEXT_COLOR, font_size=42
        ).next_to(title, DOWN, buff=0.9)
        
        equation[0][0:2].set_color(ACCENT_COLOR)  # W2
        equation[0][7:9].set_color(PRIMARY_COLOR) # W1
        
        self.play(Write(equation))
        self.wait(1)

        # 3. Vector Representation (Input state)
        # Positioned lower (DOWN * 2.2) to prevent overlap with the equation during expansion
        vector = Rectangle(
            height=1.8, width=0.9, 
            fill_color=CONTEXT_TEAL, fill_opacity=1, 
            stroke_width=0
        ).move_to(DOWN * 2.2) 
        
        dim_label = Text("d_model", color=TEXT_COLOR, font_size=18).next_to(vector, LEFT, buff=0.4)
        self.play(FadeIn(vector, shift=UP), Write(dim_label))

        # 4. Action: Expansion (First Linear Layer)
        # The vector stretches to represent the massive dimension growth
        expansion_label = Text("49,152 Dimensions", color=PRIMARY_COLOR, font_size=22, weight=BOLD)
        expansion_label.to_edge(RIGHT, buff=0.8).shift(UP * 0.5)
        
        expansion_desc = Text("(Massive Hidden Layer)", color=TEXT_COLOR, font_size=16)
        expansion_desc.next_to(expansion_label, DOWN, buff=0.2)

        # Using standard 'slow_into' rate function to avoid errors
        self.play(
            vector.animate.stretch_to_fit_height(5.5).set_fill(color=PRIMARY_COLOR),
            dim_label.animate.set_opacity(0),
            Write(expansion_label),
            Write(expansion_desc),
            run_time=2,
            rate_func=slow_into
        )
        
        self.play(Indicate(vector, color=ACCENT_COLOR), run_time=1)
        self.wait(1)

        # 5. Action: Compression (Second Linear Layer)
        # The vector returns to its original size, now containing refined "knowledge"
        final_dim_label = Text("Refined Vector", color=CONTEXT_TEAL, font_size=18).next_to(vector, LEFT, buff=0.4)

        self.play(
            vector.animate.stretch_to_fit_height(1.8).set_fill(color=CONTEXT_TEAL),
            FadeOut(expansion_label),
            FadeOut(expansion_desc),
            FadeIn(final_dim_label),
            run_time=2,
            rate_func=smooth
        )

        # 6. Final Polish: The Knowledge Box
        # Large buff (0.8) ensures the rectangle doesn't touch the title or labels
        box = SurroundingRectangle(equation, color=PRIMARY_COLOR, buff=0.8, stroke_width=2)
        self.play(Create(box))
        
        self.wait(3)

from manim import *

# --- Strictly Implemented Color Palette ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = "#fce7f3" # Light Pink
ACCENT_COLOR = "#be185d"    # Darker shade
TEXT_COLOR = "#1f2937"      # Dark Grey
WHITE_BG = "#ffffff"        # Background
CONTEXT_TEAL = "#52122f"    # Residual connection color

class Scene19AddAndNorm(Scene):
    def construct(self):
        self.camera.background_color = WHITE_BG

        # 1. Title Setup (Requirement: BLACK, NOT bold)
        title = Text(
            "", 
            color=BLACK, weight=NORMAL, font_size=32
        ).to_edge(UP, buff=0.7)
        self.add(title)

        # 2. Define the "Processing Block" (Attention or FFN)
        # Using SECONDARY_COLOR (#fce7f3) for the fill and PRIMARY_COLOR (#db2777) for stroke
        block = RoundedRectangle(
            corner_radius=0.2, height=2, width=4.5, 
            color=PRIMARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=1.0,
            stroke_width=4
        ).shift(LEFT * 0.5)
        
        block_label = Text("Attention / FFN Block", color=PRIMARY_COLOR, font_size=24, weight=BOLD).move_to(block)
        
        # 3. Define the "Add" Node
        # Redesigned junction with PRIMARY_COLOR stroke and SECONDARY_COLOR fill
        add_circle = Circle(radius=0.4, color=PRIMARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=1.0, stroke_width=4)
        add_plus = Text("+", color=PRIMARY_COLOR, font_size=40, weight=BOLD).move_to(add_circle)
        add_node = VGroup(add_circle, add_plus).next_to(block, RIGHT, buff=1.2)

        # 4. Vectors and Paths
        # Input Vector Arrow
        input_start = LEFT * 6 + block.get_y() * UP
        input_vec = Arrow(input_start, block.get_left(), color=TEXT_COLOR, buff=0.1, stroke_width=5)
        input_label = Text("Input (x)", color=TEXT_COLOR, font_size=20).next_to(input_vec, UP, buff=0.15)

        # Main path through the block
        through_path = Arrow(block.get_right(), add_node.get_left(), color=TEXT_COLOR, buff=0.1, stroke_width=5)
        result_label = Text("Block(x)", color=PRIMARY_COLOR, font_size=20).next_to(through_path, UP, buff=0.15)

        # Residual Connection (The Bypass)
        # Curved path using CONTEXT_TEAL to skip over the block
        residual_path = CurvedArrow(
            start_point=input_start + RIGHT * 0.5, 
            end_point=add_node.get_top() + UP * 0.05, 
            angle=-TAU/3.5, 
            color=CONTEXT_TEAL,
            stroke_width=6
        )
        
        residual_label = Text("Residual Connection", color=CONTEXT_TEAL, font_size=20, weight=BOLD).next_to(residual_path, UP, buff=0.3)

        # 5. Final Equation
        # Using set_color_by_tex for robust styling
        formula = MathTex(
            r"\text{Output} =", r"\text{Block}(x)", r"+", r"x",
            color=TEXT_COLOR, font_size=42
        ).to_edge(DOWN, buff=0.8)
        
        formula.set_color_by_tex(r"\text{Block}(x)", PRIMARY_COLOR)
        formula.set_color_by_tex(r"x", CONTEXT_TEAL)

        # --- Animation Sequence ---

        # Start by showing the core block and the raw input
        self.play(
            FadeIn(block, scale=0.9),
            Write(block_label),
            GrowArrow(input_vec),
            Write(input_label),
            run_time=1
        )
        self.wait(0.5)

        # Animate the processing through the block
        self.play(
            GrowArrow(through_path),
            Write(result_label),
            FadeIn(add_node, shift=LEFT * 0.5),
            run_time=0.8
        )
        self.wait(0.3)

        # Highlight the Residual Connection (The Bypass)
        self.play(
            Create(residual_path),
            Write(residual_label),
            run_time=1.2
        )
        
        # Flash the Add node to show the summation occurring
        self.play(
            Flash(add_node, color=CONTEXT_TEAL, line_length=0.3, flash_radius=0.5, num_lines=12),
            add_node.animate.scale(1.2),
            rate_func=there_and_back,
            run_time=0.5
        )
        
        # Display the final mathematical summary
        self.play(FadeIn(formula, shift=UP * 0.3), run_time=0.8)

        # Final visual pulse to emphasize the "Bypass" logic
        self.play(
            residual_path.animate.set_stroke(width=10),
            Indicate(formula.get_parts_by_tex("x"), color=CONTEXT_TEAL),
            rate_func=there_and_back,
            run_time=1.2
        )

        self.wait(2)

from manim import *

# --- Strictly Implemented Color Palette ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = "#fce7f3" # Light Pink
ACCENT_COLOR = "#be185d"    # Darker shade
TEXT_COLOR = "#1f2937"      # Dark Grey
WHITE_BG = "#ffffff"        # Background
CONTEXT_TEAL = "#ed579a"    # Residual connection color

class Scene20CompletedBlock(Scene):
    def construct(self):
        # 1. Setup Environment
        self.camera.background_color = WHITE_BG

        # 2. Component Creators (Adjusted for smaller size)
        def get_box(label_text, height=1.0):
            # Reduced height and width to save space
            box = Rectangle(
                height=height, width=4.5, 
                color=PRIMARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=1,
                stroke_width=3
            )
            lbl = Text(label_text, color=PRIMARY_COLOR, font_size=18, weight=BOLD).move_to(box)
            return VGroup(box, lbl)

        def get_add_norm():
            # Compact Add & Norm node
            circle = Circle(radius=0.25, color=ACCENT_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=3)
            plus = Text("+", color=ACCENT_COLOR, font_size=24, weight=BOLD).move_to(circle)
            label = Text("Add & Norm", color=ACCENT_COLOR, font_size=12).next_to(circle, RIGHT, buff=0.15)
            return VGroup(circle, plus, label)

        # --- Building the Stack (Bottom to Top) ---
        # Using tight buffs (0.55) to ensure vertical fit
        input_label = Text("Input Embedding", color=TEXT_COLOR, font_size=14)
        
        mha = get_box("Multi-Head Attention", height=1.1)
        mha.next_to(input_label, UP, buff=0.55)

        an1 = get_add_norm()
        an1.next_to(mha, UP, buff=0.55)

        ffn = get_box("Feed-Forward Network (FFN)", height=0.9)
        ffn.next_to(an1, UP, buff=0.55)

        an2 = get_add_norm()
        an2.next_to(ffn, UP, buff=0.55)

        output_label = Text("Refined Context Vectors", color=CONTEXT_TEAL, font_size=14)
        output_label.next_to(an2, UP, buff=0.55)

        # Group and center the schematic
        schematic = VGroup(input_label, mha, an1, ffn, an2, output_label).center()

        # --- Main Flow Arrows ---
        arrow_config = {"color": TEXT_COLOR, "buff": 0.08, "stroke_width": 2.5, "max_tip_length_to_length_ratio": 0.12}
        
        main_path = VGroup(
            Arrow(input_label.get_top(), mha.get_bottom(), **arrow_config),
            Arrow(mha.get_top(), an1[0].get_bottom(), **arrow_config),
            Arrow(an1[0].get_top(), ffn.get_bottom(), **arrow_config),
            Arrow(ffn.get_top(), an2[0].get_bottom(), **arrow_config),
            Arrow(an2[0].get_top(), output_label.get_bottom(), **arrow_config)
        )

        # --- Residual Paths (Tighter horizontal offset) ---
        res_offset = 2.6
        # Residual 1: Skip MHA
        res1_start = main_path[0].get_center()
        res1_path = VMobject(color=CONTEXT_TEAL, stroke_width=3)
        res1_path.set_points_as_corners([
            res1_start,
            res1_start + LEFT * res_offset,
            [res1_start[0] - res_offset, an1[0].get_y(), 0],
            an1[0].get_left()
        ])
        res1_tip = Arrow(res1_path.get_end() + LEFT*0.05, an1[0].get_left(), color=CONTEXT_TEAL, buff=0, stroke_width=3)

        # Residual 2: Skip FFN
        res2_start = main_path[2].get_center()
        res2_path = VMobject(color=CONTEXT_TEAL, stroke_width=3)
        res2_path.set_points_as_corners([
            res2_start,
            res2_start + LEFT * res_offset,
            [res2_start[0] - res_offset, an2[0].get_y(), 0],
            an2[0].get_left()
        ])
        res2_tip = Arrow(res2_path.get_end() + LEFT*0.05, an2[0].get_left(), color=CONTEXT_TEAL, buff=0, stroke_width=3)

        # --- Animation Sequence ---
        self.play(Write(input_label))
        
        self.play(
            AnimationGroup(Create(mha), Create(ffn), lag_ratio=0.3),
            run_time=1.2
        )
        
        self.play(
            AnimationGroup(Create(an1), Create(an2), lag_ratio=0.3),
            run_time=1.0
        )

        self.play(LaggedStart(*[GrowArrow(a) for a in main_path], lag_ratio=0.2))
        
        # Residual reveals with visual "Add" feedback
        self.play(Create(res1_path), GrowArrow(res1_tip), run_time=1.2)
        self.play(Flash(an1[0], color=CONTEXT_TEAL, flash_radius=0.3, num_lines=8), run_time=0.5)

        self.play(Create(res2_path), GrowArrow(res2_tip), run_time=1.2)
        self.play(Flash(an2[0], color=CONTEXT_TEAL, flash_radius=0.3, num_lines=8), run_time=0.5)
        
        self.play(FadeIn(output_label, shift=UP*0.2))
        
        self.wait(3)

from manim import *

# --- Visual Styling Constants ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = WHITE      # Background
ACCENT_COLOR = "#be185d"    # Darker Pink
TEXT_COLOR = "#1f2937"      # Dark Grey/Black for labels
CONTEXT_TEAL = "#0d9488"    # Residual/Vector color

class Scene21DeepStacking(MovingCameraScene):
    def construct(self):
        # 1. Setup Environment
        self.camera.background_color = SECONDARY_COLOR

        # --- Component Creator ---
        def get_block_visual(height=1.0, width=4.5, is_thin=False):
            fill_opacity = 0.5 if is_thin else 0.8
            stroke_width = 1 if is_thin else 2
            
            box = Rectangle(
                height=height, width=width,
                color=PRIMARY_COLOR, 
                fill_color=ACCENT_COLOR, 
                fill_opacity=fill_opacity,
                stroke_width=stroke_width
            )
            return box

        # --- Scene Layout ---
        
        # 1. Transformer Block 1 (Bottom)
        base_block = get_block_visual().shift(DOWN * 1.5)
        base_label = Text("Transformer Block 1", color=PRIMARY_COLOR, font_size=18)
        base_label.next_to(base_block, LEFT, buff=0.8)

        # 2. Input Words
        input_words = ["The", "cat", "sat", "on", "the"]
        input_dots = VGroup(*[
            VGroup(
                Dot(color=CONTEXT_TEAL, radius=0.1),
                # Using TEXT_COLOR (Black) for regular text
                Text(word, color=TEXT_COLOR, font_size=14).next_to(Dot(), DOWN, buff=0.2)
            ) for word in input_words
        ]).arrange(RIGHT, buff=0.5).next_to(base_block, DOWN, buff=1.0)

        # 3. The Middle Stack (Layers 2-95)
        num_visual_layers = 20 
        stack = VGroup()
        for i in range(num_visual_layers):
            layer = get_block_visual(height=0.12, width=4.5, is_thin=True)
            layer.move_to(base_block.get_top() + UP * (i * 0.18 + 0.1))
            stack.add(layer)

        # 4. Transformer Block 96 (Top)
        top_block = get_block_visual().move_to(stack.get_top() + UP * 0.6)
        top_label = Text("Transformer Block 96", color=PRIMARY_COLOR, font_size=18)
        top_label.next_to(top_block, LEFT, buff=0.8)
        
        tower_group = VGroup(base_block, stack, top_block)

        # 5. Left Side Brace for the stack
        stack_brace = Brace(stack, LEFT, color=PRIMARY_COLOR, buff=0.3)
        stack_text = Text("x96 Layers Total", color=PRIMARY_COLOR, font_size=20).next_to(stack_brace, LEFT)

        # --- Animation Sequence ---

        # Step 1: Show the Foundation
        self.play(
            Create(base_block), 
            FadeIn(input_dots), 
            Write(base_label)
        )
        self.wait(1)

        # Step 2: Architecture Expansion & Zoom
        # We zoom out to see the full "skyscrapers" of blocks
        self.play(
            LaggedStart(
                *[FadeIn(layer, shift=UP*0.1) for layer in stack],
                FadeIn(top_block, shift=UP*0.1),
                lag_ratio=0.05
            ),
            self.camera.frame.animate.scale(1.45).move_to(tower_group.get_center() + UP*0.5),
            run_time=4,
            rate_func=smooth
        )

        # Step 3: Show Top Label and Scale Indicator
        self.play(
            Write(top_label),
            GrowFromCenter(stack_brace), 
            Write(stack_text)
        )
        self.wait(1)

        # Step 4: Data Flow
        flowing_data = input_dots.copy()
        self.play(
            flowing_data.animate.move_to(top_block.get_center()).set_opacity(0.3),
            run_time=3,
            rate_func=linear
        )

        # Step 5: Final Title
        output_label = Text("Contextual Embeddings", color=TEXT_COLOR, font_size=24)
        output_label.next_to(top_block, UP, buff=1.0)
        self.play(Write(output_label))
        
        self.wait(3)

from manim import *

# --- Visual Styling Constants ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = WHITE      # Requested Background
ACCENT_COLOR = "#be185d"    # Darker Pink
GOLD_COLOR = "#db2777"      # Deep Gold (Adjusted for white background)
TEXT_COLOR = BLACK          # Black for titles and labels
CONTEXT_TEAL = "#0d9488"    # Vector color

class Scene22FinalVector(MovingCameraScene):
    def construct(self):
        # 1. Setup Environment
        self.camera.background_color = SECONDARY_COLOR

        # --- Component Creator ---
        def get_block_visual(height=1.0, width=4.5):
            return Rectangle(
                height=height, width=width,
                color=PRIMARY_COLOR, 
                fill_color=ACCENT_COLOR, 
                fill_opacity=0.8,
                stroke_width=2
            )

        # --- Scene Layout ---
        # Representing the top of the tower
        top_block = get_block_visual().shift(DOWN * 0.5)
        
        # Block Label (Left side, Not Bold)
        top_label = Text("Transformer Block 96", color=PRIMARY_COLOR, font_size=20)
        top_label.next_to(top_block, LEFT, buff=0.8)

        # Output vectors (dots) 
        words = ["The", "cat", "sat", "on", "the"]
        vectors = VGroup(*[
            VGroup(
                Dot(color=CONTEXT_TEAL, radius=0.15),
                Text(word, color=TEXT_COLOR, font_size=16).next_to(Dot(), DOWN, buff=0.2)
            ) for word in words
        ]).arrange(RIGHT, buff=0.7).next_to(top_block, UP, buff=1.0)

        # Isolating the final vector for the word "the"
        final_vector_group = vectors[-1]
        final_dot = final_vector_group[0]
        final_word = final_vector_group[1]
        
        # --- Animation Sequence ---

        # Step 1: Establish the final stage
        self.camera.frame.scale(1.2).move_to(top_block.get_center() + UP * 1.5)
        self.add(top_block, top_label, vectors)
        self.wait(1)

        # Step 2: The Transformation Focus
        # We use a subtle shadow/indication to show focus
        self.play(
            Indicate(final_vector_group, color=PRIMARY_COLOR, scale_factor=1.1),
            run_time=1.5
        )

        # Step 3: The Golden Summation
        # The dot transforms into a gold "Sum" of the context
        self.play(
            final_dot.animate.set_color(GOLD_COLOR).scale(1.4),
            final_word.animate.set_color(GOLD_COLOR).scale(1.2),
            Flash(final_dot, color=GOLD_COLOR, line_length=0.3, num_lines=12),
            run_time=1.5
        )

        # Step 4: Visualizing the "Mathematical Sum"
        # Lines representing data from previous words converging into the final one
        convergence_lines = VGroup()
        for i in range(len(vectors) - 1):
            line = Line(
                vectors[i][0].get_center(), 
                final_dot.get_center(), 
                stroke_width=2, 
                color=CONTEXT_TEAL
            ).set_opacity(0.2)
            convergence_lines.add(line)

        # Equation for "The Sum of the Story"
        sum_label = Text("Mathematical Sum of Context", color=GOLD_COLOR, font_size=22)
        sum_label.next_to(vectors, UP, buff=1.0)
        
        sum_formula = MathTex(
            r"\mathbf{h}_{final} = \text{Softmax}(QK^T)V",
            color=TEXT_COLOR,
            font_size=30
        ).next_to(sum_label, UP, buff=0.3)

        self.play(
            Create(convergence_lines),
            Write(sum_label),
            Write(sum_formula),
            run_time=2
        )

        # Step 5: Final Glow Pulse
        self.play(
            final_dot.animate.scale(1.2),
            rate_func=there_and_back,
            run_time=1
        )
        
        self.wait(3)


from manim import *
import numpy as np

# --- Visual Styling Constants ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = WHITE      # Background
ACCENT_COLOR = "#be185d"    # Darker Pink
GOLD_COLOR = "#76093a"      # Gold for the final vector
TEXT_COLOR = BLACK          # For titles and equations

class Scene23Unembedding(Scene):
    def construct(self):
        # 1. Setup Environment
        self.camera.background_color = SECONDARY_COLOR

        # --- Element Creation ---
        
        # The Final "Gold" Vector (Representing the hidden state)
        vector_box = Rectangle(
            height=3, 
            width=0.6, 
            color=GOLD_COLOR, 
            fill_opacity=0.8, 
            fill_color=GOLD_COLOR
        )
        vector_label = MathTex(r"\vec{v}_{final}", color=GOLD_COLOR).next_to(vector_box, DOWN)
        vector_group = VGroup(vector_box, vector_label).shift(LEFT * 4)

        # Multiplication Sign
        times_sign = MathTex(r"\times", color=TEXT_COLOR, font_size=60).shift(LEFT * 2.5)

        # The Transposed Embedding Matrix (E^T)
        matrix_rect = Rectangle(height=4, width=3.5, color=PRIMARY_COLOR, stroke_width=2)
        
        # Creating grid lines to represent the vocabulary vectors
        matrix_rows = VGroup(*[
            Line(
                matrix_rect.get_left() + UP * i, 
                matrix_rect.get_right() + UP * i, 
                color=PRIMARY_COLOR, 
                stroke_width=1
            )
            for i in np.arange(-1.5, 2, 0.5)
        ])
        
        # Label for the matrix: E transposed
        matrix_label = MathTex(r"E^T", color=PRIMARY_COLOR).next_to(matrix_rect, UP, buff=0.3)
        matrix_desc = Text("Embedding Matrix (Transpose)", color=PRIMARY_COLOR, font_size=18)
        matrix_desc.next_to(matrix_label, UP, buff=0.1)
        
        matrix_group = VGroup(matrix_rect, matrix_rows, matrix_label, matrix_desc).shift(RIGHT * 0.5)

        # Equals Sign and Resulting Logits
        equals_sign = MathTex(r"=", color=TEXT_COLOR, font_size=60).shift(RIGHT * 3)
        logits_box = Rectangle(
            height=4, 
            width=0.6, 
            color=ACCENT_COLOR, 
            fill_opacity=0.2, 
            stroke_width=2
        ).shift(RIGHT * 4.5)
        logits_label = Text("Logits", color=ACCENT_COLOR, font_size=20).next_to(logits_box, DOWN)

        # --- Animation Sequence ---

        # Step 1: Introduce the Vector and the Mathematical Operation
        self.play(
            FadeIn(vector_group, shift=RIGHT),
            Write(times_sign)
        )
        self.wait(0.5)

        # Step 2: Reveal the massive Embedding Matrix
        self.play(
            Create(matrix_rect),
            LaggedStart(*[Create(row) for row in matrix_rows], lag_ratio=0.05),
            Write(matrix_desc),
            Write(matrix_label)
        )
        self.wait(1)

        # Step 3: Visualizing the "Dot Product" Scan
        # A semi-transparent copy of the vector moves across the matrix rows
        scanning_vector = vector_box.copy().set_opacity(0.3)
        
        self.play(Write(equals_sign), FadeIn(logits_box), FadeIn(logits_label))

        # Start the scanning movement
        self.play(
            scanning_vector.animate.move_to(matrix_rect.get_left() + RIGHT * 0.3),
            run_time=0.5
        )
        
        # The scan across the matrix simulates the calculation of scores for every word
        self.play(
            scanning_vector.animate.move_to(matrix_rect.get_right() - RIGHT * 0.3),
            logits_box.animate.set_opacity(0.8).set_fill(ACCENT_COLOR, opacity=0.5),
            run_time=2,
            rate_func=linear
        )
        self.play(FadeOut(scanning_vector))

        # Step 4: Final Mathematical Summary (Bottom Positioned)
        # Using r"" strings for LaTeX and ensuring black text
        formula = MathTex(
            r"\text{Score} = \vec{v}_{final} \cdot E^T",
            color=TEXT_COLOR, 
            font_size=36
        ).to_edge(DOWN, buff=0.6)

        self.play(Write(formula))
        
        # Step 5: Highlight a matching word (The "Winner")
        match_highlight = Rectangle(
            height=0.5, 
            width=3.5, 
            color=GOLD_COLOR, 
            fill_opacity=0.3, 
            stroke_width=0
        ).move_to(matrix_rect.get_center() + UP * 0.75)
        
        self.play(
            FadeIn(match_highlight),
            Indicate(logits_box, color=GOLD_COLOR)
        )

        self.wait(3)

from manim import *

# --- Visual Styling Constants ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = WHITE      # Background
ACCENT_COLOR = "#be185d"    # Darker Pink
TEXT_COLOR = "#1f2937"      # Dark Grey/Black
GRID_COLOR = "#e5e7eb"      # Light grey for background

class Scene24LogitsFixed(Scene):
    def construct(self):
        # 1. Setup Environment
        self.camera.background_color = SECONDARY_COLOR
        
        # Subtle technical background grid
        grid = NumberPlane(
            background_line_style={
                "stroke_color": GRID_COLOR,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        self.add(grid)

        # --- Scene Elements ---
        
        # Title with a professional non-bold look and underline
        title = Text("Logits: Raw Prediction Scores", color=TEXT_COLOR, font_size=36)
        title.to_edge(UP, buff=1.0)
        underline = Line(LEFT, RIGHT, color=PRIMARY_COLOR, stroke_width=2).scale(3)
        underline.next_to(title, DOWN, buff=0.1)

        # Data definition (removed the ellipsis)
        logit_data = [
            ("dog", "1.8"),
            ("car", "0.4"),
            ("mat", "4.1"),
            ("water", "1.0")
        ]

        # Table Creation: Using two separate columns to prevent jitter
        # Monospace ensures that digits and signs (- or .) don't shift the layout
        word_col = VGroup()
        score_col = VGroup()
        
        for word, score in logit_data:
            w_txt = Text(f"{word}:", color=TEXT_COLOR, font_size=32)
            # 'Monospace' is a safe cross-platform alias that prevents jitter
            s_txt = Text(score, color=PRIMARY_COLOR, font_size=32, font="Monospace")
            word_col.add(w_txt)
            score_col.add(s_txt)

        # Alignments: words right-aligned, scores left-aligned
        word_col.arrange(DOWN, buff=0.6, aligned_edge=RIGHT)
        score_col.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        
        # Lock them together with a fixed buffer
        score_col.next_to(word_col, RIGHT, buff=0.8)
        table_group = VGroup(word_col, score_col).move_to(ORIGIN)

        # --- Animation Sequence ---

        # Step 1: Title
        self.play(
            Write(title),
            Create(underline),
            run_time=1.2
        )
        self.wait(0.5)

        # Step 2: Reveal Logits (Row by Row)
        # Using simple FadeIn for words and Write for numbers to keep them stable
        for i in range(len(logit_data)):
            self.play(
                FadeIn(word_col[i], shift=RIGHT * 0.2),
                Write(score_col[i]), 
                run_time=0.6
            )

        self.wait(1)

        # Step 3: Highlight the Winner (mat: 15.8)
        winner_index = 2
        winner_row = VGroup(word_col[winner_index], score_col[winner_index])
        
        highlight_box = SurroundingRectangle(
            winner_row, 
            color=ACCENT_COLOR, 
            buff=0.3, 
            stroke_width=2,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.1
        )
        
        winner_label = Text("Highest Probability", color=ACCENT_COLOR, font_size=20)
        winner_label.next_to(highlight_box, RIGHT, buff=0.5)

        self.play(
            Create(highlight_box),
            Write(winner_label),
            score_col[winner_index].animate.set_color(ACCENT_COLOR).scale(1.1),
            run_time=1
        )
        
        # Step 4: Final Footer
        footer = Text(
            "Final  layer output before Softmax activation.",
            color=TEXT_COLOR,
            font_size=18,
            slant=ITALIC
        ).to_edge(DOWN, buff=1.0)
        
        self.play(FadeIn(footer, shift=UP * 0.3))
        self.wait(3)

from manim import *

# --- Visual Styling Constants ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = WHITE      # Background
ACCENT_COLOR = "#be185d"    # Darker Pink
TEXT_COLOR = "#1f2937"      # Dark Grey/Black
GRID_COLOR = "#e5e7eb"      # Light grey

class Scene25Softmax(Scene):
    def construct(self):
        # 1. Setup Environment
        self.camera.background_color = SECONDARY_COLOR
        
        # --- Scene Elements ---
        
        # Title (NOT bold, Black)
        title = Text("Softmax: Probability Distribution", color=BLACK, font_size=34)
        title.to_edge(UP, buff=0.8)
        underline = Line(LEFT, RIGHT, color=PRIMARY_COLOR, stroke_width=2).scale(3.5)
        underline.next_to(title, DOWN, buff=0.1)

        # Corrected mathematical data
        # Math: P(i) = exp(logit_i) / sum(exp(logits))
        data = [
            ("dog", "1.8", "9%"),
            ("car", "0.4", "2%"),
            ("mat", "4.1", "86%"),
            ("water", "1.0", "3%")
        ]

        # Column Groups for stable layout
        word_col = VGroup()
        logit_col = VGroup()
        arrow_col = VGroup()
        percent_col = VGroup()
        
        for word, logit, percent in data:
            word_col.add(Text(f"{word}:", color=TEXT_COLOR, font_size=30))
            # Monospace prevents horizontal jitter during reveal
            logit_col.add(Text(logit, color=TEXT_COLOR, font_size=30, font="Monospace"))
            arrow_col.add(MathTex(r"\rightarrow", color=PRIMARY_COLOR))
            percent_col.add(Text(percent, color=PRIMARY_COLOR, font_size=30, font="Monospace"))

        # Align columns independently to maintain strict spacing
        word_col.arrange(DOWN, buff=0.7, aligned_edge=RIGHT)
        logit_col.arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        arrow_col.arrange(DOWN, buff=0.7)
        percent_col.arrange(DOWN, buff=0.7, aligned_edge=LEFT)

        # Assemble the table
        logit_col.next_to(word_col, RIGHT, buff=0.6)
        arrow_col.next_to(logit_col, RIGHT, buff=0.6)
        percent_col.next_to(arrow_col, RIGHT, buff=0.6)
        
        table_group = VGroup(word_col, logit_col, arrow_col, percent_col).move_to(ORIGIN)

        # Softmax Equation at the bottom
        formula = MathTex(
            r"\sigma(z)_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}",
            color=BLACK,
            font_size=38
        ).to_edge(DOWN, buff=0.8)

        # --- Animation Sequence ---

        # Step 1: Display Initial State (Logits)
        self.add(title, underline)
        self.play(
            FadeIn(word_col, shift=UP * 0.1),
            Write(logit_col),
            run_time=1.5
        )
        self.wait(0.5)

        # Step 2: Introduce the Math
        self.play(Write(formula), run_time=1)
        self.wait(1)

        # Step 3: Transform (The Softmax Activation)
        # We process row-by-row to show the conversion
        for i in range(len(data)):
            self.play(
                Create(arrow_col[i]),
                Write(percent_col[i]),
                logit_col[i].animate.set_opacity(0.3),
                run_time=0.6
            )

        self.wait(1)

        # Step 4: Highlighting the Mathematically Correct Winner
        winner_index = 2 # "mat" (86%)
        winner_box = SurroundingRectangle(
            VGroup(word_col[winner_index], percent_col[winner_index]),
            color=PRIMARY_COLOR,
            buff=0.3,
            stroke_width=2
        )
        
        winner_tag = Text("Confidence: 86%", color=PRIMARY_COLOR, font_size=22)
        winner_tag.next_to(winner_box, RIGHT, buff=0.5)

        self.play(
            Create(winner_box),
            Write(winner_tag),
            percent_col[winner_index].animate.scale(1.2),
            run_time=1.2
        )

        self.wait(3)

from manim import *

# --- Visual Styling Constants ---
PRIMARY_COLOR = "#db2777"   # Pinkish-Red
SECONDARY_COLOR = WHITE      # Background
ACCENT_COLOR = "#be185d"    # Darker Pink
TEXT_COLOR = BLACK          # Standard non-bold titles/text

class Scene26Selection(Scene):
    def construct(self):
        # 1. Setup Environment
        self.camera.background_color = SECONDARY_COLOR

        # --- Scene Elements ---
        
        # Leading candidate from the Softmax results
        word_text = Text("mat", color=TEXT_COLOR, font_size=72)
        
        # Confidence score (Secondary visual)
        prob_text = Text("Confidence: 86%", color=PRIMARY_COLOR, font_size=24)
        prob_text.next_to(word_text, DOWN, buff=0.5)
        
        selection_group = VGroup(word_text, prob_text).move_to(ORIGIN)

        # A clean frame to focus the eye initially
        initial_frame = SurroundingRectangle(
            selection_group, 
            color=PRIMARY_COLOR, 
            buff=0.5, 
            stroke_width=2
        )

        # --- Animation Sequence ---

        # Step 1: Presentation of the Winner
        self.play(
            Write(word_text),
            FadeIn(prob_text, shift=UP * 0.2),
            Create(initial_frame),
            run_time=1.2
        )
        self.wait(0.5)

        # Step 2: The Final Selection (Highlight and Expand)
        # We use 'smooth' here for maximum compatibility across all Manim versions
        self.play(
            # The word grows and takes the primary brand color
            word_text.animate.scale(2.2).set_color(PRIMARY_COLOR),
            
            # Clear the UI elements to focus on the result
            FadeOut(prob_text, shift=DOWN * 0.3),
            FadeOut(initial_frame),
            
            run_time=1.5,
            rate_func=smooth
        )

        # Step 3: The "Success" Flash
        # This adds the 'awesome' factor by simulating a mathematical confirmation
        self.play(
            Flash(
                word_text, 
                color=PRIMARY_COLOR, 
                line_length=0.4, 
                num_lines=15, 
                flash_radius=1.2,
                time_width=0.3
            )
        )

        # Step 4: Final Labeling
        final_label = Text("Final Output Selected", color=TEXT_COLOR, font_size=20)
        final_label.next_to(word_text, DOWN, buff=1.0)
        self.play(FadeIn(final_label, shift=UP * 0.2))

        self.wait(3)

from manim import *
import random

# --- Visual Styling Constants ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
KEY_COLOR = "#e5e7eb"          # Light grey for keys
SCREEN_BG_COLOR = WHITE

class Scene27RealisticLoopFinal(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- 1. AMBIENT BACKGROUND PARTICLES ---
        particles = VGroup()
        for _ in range(30):
            p = Circle(
                radius=random.uniform(0.05, 0.2), 
                fill_color=PRIMARY_COLOR, 
                fill_opacity=random.uniform(0.05, 0.15), 
                stroke_width=0
            ).move_to([random.uniform(-7, 7), random.uniform(-4, 4), 0])
            
            velocity = np.array([random.uniform(-0.15, 0.15), random.uniform(-0.15, 0.15), 0])
            p.add_updater(lambda m, dt, v=velocity: m.shift(v * dt))
            particles.add(p)
        self.add(particles)

        # --- 2. PHONE STRUCTURE ---
        phone_frame = RoundedRectangle(
            corner_radius=0.4, height=7.8, width=4.2,
            fill_color=PRIMARY_COLOR, fill_opacity=1, stroke_width=0
        ).set_z_index(1)
        
        screen = RoundedRectangle(
            corner_radius=0.2, height=7.4, width=3.9,
            fill_color=SCREEN_BG_COLOR, fill_opacity=1, stroke_width=0
        ).move_to(phone_frame.get_center()).set_z_index(2)

        # Content (Cat Image)
        try:
            cat_photo = ImageMobject(r"D:\manim\cat.png") 
            cat_photo.width = 3.3
            cat_photo.move_to(screen.get_top() + DOWN * 1.6).set_z_index(3)
        except:
            cat_photo = RoundedRectangle(corner_radius=0.1, height=2.2, width=3.3, color=GRAY, fill_opacity=0.1)
            cat_photo.move_to(screen.get_top() + DOWN * 1.6).set_z_index(3)

        input_box = RoundedRectangle(
            corner_radius=0.1, height=0.6, width=3.5,
            fill_color=WHITE, fill_opacity=1, stroke_color=LIGHT_GREY, stroke_width=1.5
        ).next_to(cat_photo, DOWN, buff=0.4).set_z_index(3)

        # --- 3. KEYBOARD & SUGGESTION SETS ---
        keyboard = self.get_keyboard().move_to(screen.get_bottom() + UP * 1.3).set_z_index(3)

        # Suggestion Set 1 (High Z-Index to ensure visibility)
        suggestions_1 = self.get_suggestions(["mat", "rug", "floor"])
        suggestions_1.next_to(keyboard, UP, buff=0.2).set_z_index(50)
        
        # Suggestion Set 2 (The Loop)
        suggestions_2 = self.get_suggestions(["quietly", "happily", "peacefully"])
        suggestions_2.next_to(keyboard, UP, buff=0.2).set_z_index(50)

        # --- 4. ANIMATION SEQUENCE ---
        self.add(phone_frame, screen, cat_photo, keyboard, input_box)

        # --- TYPING PHASE 1: Character-by-Character ---
        text_anchor = input_box.get_left() + RIGHT * 0.2
        typed_text = Text("The cat sat on the ", font_size=16, color=TEXT_COLOR)
        typed_text.move_to(text_anchor, aligned_edge=LEFT).set_z_index(60)

        # Cursor logic
        cursor = Line(ORIGIN, UP*0.3, color=PRIMARY_COLOR, stroke_width=2).set_z_index(60)
        cursor.add_updater(lambda m: m.next_to(typed_text, RIGHT, buff=0.05))
        self.add(cursor)

        # Realistic Typing Animation
        self.play(AddTextLetterByLetter(typed_text), run_time=2.5, rate_func=linear)
        
        # Reveal suggestions with a fade-in and slide
        self.play(FadeIn(suggestions_1, shift=UP*0.2), run_time=0.6)
        self.wait(0.5)

        # Selection highlight
        self.play(
            suggestions_1[0][0].animate.set_fill(PRIMARY_COLOR),
            suggestions_1[0][1].animate.set_color(WHITE),
            run_time=0.3
        )

        # --- TYPING PHASE 2: The Addition ---
        updated_text_1 = Text("The cat sat on the mat ", font_size=16, color=TEXT_COLOR)
        updated_text_1.move_to(text_anchor, aligned_edge=LEFT).set_z_index(60)

        self.play(
            Transform(typed_text, updated_text_1),
            FadeOut(suggestions_1, shift=UP*0.2),
            run_time=0.4
        )

        # New suggestions for the next word
        self.play(FadeIn(suggestions_2, shift=UP*0.2), run_time=0.6)
        self.wait(0.5)

        # Select 'peacefully'
        self.play(
            suggestions_2[2][0].animate.set_fill(PRIMARY_COLOR),
            suggestions_2[2][1].animate.set_color(WHITE),
            run_time=0.3
        )

        # Final sentence typing
        final_sentence = Text("The cat sat on the mat peacefully", font_size=16, color=TEXT_COLOR)
        final_sentence.move_to(text_anchor, aligned_edge=LEFT).set_z_index(60)
        
        # Scaling logic to keep "peacefully" in bounds
        if final_sentence.width > (input_box.width - 0.4):
            final_sentence.scale_to_fit_width(input_box.width - 0.4)
            final_sentence.move_to(text_anchor, aligned_edge=LEFT)

        self.play(Transform(typed_text, final_sentence), run_time=0.6)
        
        # Conclusion
        title = Text("", color=BLACK, font_size=24)
        title.to_edge(UP, buff=0.5).set_z_index(60)
        self.play(Write(title))

        self.wait(3)

    # --- HELPER METHODS ---
    def get_keyboard(self):
        rows = [["Q","W","E","R","T","Y","U","I","O","P"], ["A","S","D","F","G","H","J","K","L"], ["Z","X","C","V","B","N","M"]]
        kb = VGroup()
        for row in rows:
            r = VGroup(*[VGroup(
                RoundedRectangle(corner_radius=0.05, height=0.45, width=0.32, fill_color=KEY_COLOR, fill_opacity=1, stroke_width=0), 
                Text(l, font_size=14, color=TEXT_COLOR)
            ) for l in row]).arrange(RIGHT, 0.06)
            kb.add(r)
        sb = RoundedRectangle(corner_radius=0.05, height=0.4, width=2.2, fill_color=KEY_COLOR, fill_opacity=1, stroke_width=0)
        return VGroup(kb.arrange(DOWN, 0.1), sb).arrange(DOWN, 0.1)

    def get_suggestions(self, words):
        s_group = VGroup()
        for w in words:
            rect = RoundedRectangle(corner_radius=0.1, height=0.5, width=1.1, fill_color=SECONDARY_COLOR, fill_opacity=1, stroke_width=0)
            lbl = Text(w, font_size=14, color=PRIMARY_COLOR)
            s_group.add(VGroup(rect, lbl))
        return s_group.arrange(RIGHT, buff=0.12)

from manim import *
import random
import numpy as np

# --- Visual Styling Constants ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = WHITE        # Background
ACCENT_COLOR = "#be185d"       # Darker Pink
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
MATRIX_COLOR = "#9ca3af"       # Grey for grid lines

class Scene28and29FinalSummary(Scene):
    def construct(self):
        # 1. Setup Environment
        self.camera.background_color = SECONDARY_COLOR

        # =========================================
        # SCENE 28: THE SUMMARY MONTAGE
        # =========================================
        
        # --- Titles (NOT Bold, Black) ---
        summary_title = Text("The Calculus of Language", color=BLACK, font_size=32)
        summary_title.to_edge(UP, buff=0.8)

        # 1. Input Side (The Cat)
        input_label = Text("Input Sequence", color=TEXT_COLOR, font_size=18)
        input_text = Text("'The cat sat on the...'", color=PRIMARY_COLOR, font_size=20)
        input_group = VGroup(input_label, input_text).arrange(DOWN, buff=0.2)
        input_box = RoundedRectangle(corner_radius=0.1, height=1.2, width=3.0, color=PRIMARY_COLOR, stroke_width=2)
        full_input = VGroup(input_box, input_group).to_edge(LEFT, buff=0.8)

        # 2. Math Side (Dot Products)
        matrix_rect = Rectangle(height=2.0, width=2.0, color=MATRIX_COLOR, stroke_width=1)
        # Create a dense grid to represent billions of parameters
        grid_lines = VGroup(*[
            Line(matrix_rect.get_left() + UP*i, matrix_rect.get_right() + UP*i, color=MATRIX_COLOR, stroke_width=0.5)
            for i in np.arange(-1.0, 1.1, 0.25)
        ] + [
            Line(matrix_rect.get_top() + RIGHT*i, matrix_rect.get_bottom() + RIGHT*i, color=MATRIX_COLOR, stroke_width=0.5)
            for i in np.arange(-1.0, 1.1, 0.25)
        ])
        math_label = Text("175B Parameters", color=TEXT_COLOR, font_size=14).next_to(matrix_rect, DOWN, buff=0.2)
        math_group = VGroup(matrix_rect, grid_lines, math_label).move_to(ORIGIN)

        # 3. Output Side (The Word)
        output_label = Text("Next Word", color=TEXT_COLOR, font_size=18)
        output_word = Text("mat", color=PRIMARY_COLOR, font_size=28)
        output_group = VGroup(output_label, output_word).arrange(DOWN, buff=0.2)
        output_box = RoundedRectangle(corner_radius=0.1, height=1.2, width=2.0, color=PRIMARY_COLOR, stroke_width=2)
        full_output = VGroup(output_box, output_group).to_edge(RIGHT, buff=0.8)

        # --- Animation Sequence 28 ---
        self.play(Write(summary_title))
        self.play(
            FadeIn(full_input, shift=RIGHT),
            run_time=1
        )
        self.wait(0.5)

        # Flow from Input to Matrix
        arrow_1 = Arrow(full_input.get_right(), math_group.get_left(), color=PRIMARY_COLOR, buff=0.2)
        self.play(GrowArrow(arrow_1), FadeIn(math_group, shift=RIGHT))
        
        # Matrix "Thinking" effect (dot product simulation)
        flash_line = Line(matrix_rect.get_left(), matrix_rect.get_right(), color=PRIMARY_COLOR, stroke_width=4).set_opacity(0)
        self.play(
            flash_line.animate.set_opacity(0.6).move_to(matrix_rect.get_top()),
            flash_line.animate.move_to(matrix_rect.get_bottom()).set_opacity(0),
            run_time=1.5,
            rate_func=smooth
        )

        # Flow to Output
        arrow_2 = Arrow(math_group.get_right(), full_output.get_left(), color=PRIMARY_COLOR, buff=0.2)
        self.play(GrowArrow(arrow_2), FadeIn(full_output, shift=RIGHT))
        self.play(Indicate(output_word, color=PRIMARY_COLOR))
        self.wait(2)

        # Clear for Scene 29
        self.play(FadeOut(full_input), FadeOut(math_group), FadeOut(full_output), FadeOut(arrow_1), FadeOut(arrow_2), FadeOut(summary_title))

        # =========================================
        # SCENE 29: THE MIRACLE OF SCALE
        # =========================================
        
        miracle_title = Text("The Miracle of Scale", color=BLACK, font_size=32)
        miracle_title.to_edge(UP, buff=0.8)

        # Create a massive "cloud" of parameters (dots)
        dots = VGroup(*[
            Dot(radius=0.03, color=PRIMARY_COLOR, fill_opacity=random.uniform(0.2, 0.6))
            for _ in range(800)
        ])
        for d in dots:
            d.move_to([random.uniform(-5, 5), random.uniform(-3, 2), 0])

        scale_text = Text("175,000,000,000 Parameters", color=PRIMARY_COLOR, font_size=24)
        scale_text.next_to(miracle_title, DOWN, buff=0.5)

        # Final result sentence
        final_sentence = Text("The cat sat on the mat.", color=TEXT_COLOR, font_size=28)
        final_box = RoundedRectangle(corner_radius=0.2, height=1.0, width=6.0, color=PRIMARY_COLOR, stroke_width=2)
        final_group = VGroup(final_box, final_sentence).move_to(DOWN*0.5)

        # --- Animation Sequence 29 ---
        self.play(Write(miracle_title))
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.005),
            Write(scale_text),
            run_time=3
        )
        self.wait(1)

        # Convergence: The Miracle
        # All dots fly into the center to reveal the simple sentence
        self.play(
            dots.animate.move_to(final_group.get_center()).set_opacity(0).scale(0.1),
            ReplacementTransform(scale_text, final_group),
            run_time=3,
            rate_func=smooth # Replaced ease_in_out_expo for stability
        )
        
        self.play(Circumscribe(final_group, color=PRIMARY_COLOR, fade_out=True))
        self.wait(3)

from manim import *
import random
import numpy as np

# --- Visual Styling Constants ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
BG_COLOR = WHITE               # Professional White
TEXT_COLOR = "#1f2937"         # Dark Grey
FRAME_COLOR = "#fbcfe8"        # Light Pink

class Scene30ConclusionFixed(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- 1. AMBIENT BACKGROUND PARTICLES ---
        # Adds "appeal" and depth to the white background
        particles = VGroup()
        for _ in range(25):
            p = Circle(
                radius=random.uniform(0.05, 0.15), 
                fill_color=PRIMARY_COLOR, 
                fill_opacity=random.uniform(0.05, 0.12), 
                stroke_width=0
            ).move_to([random.uniform(-7, 7), random.uniform(-4, 4), 0])
            
            # Slow drifting movement
            velocity = np.array([random.uniform(-0.08, 0.08), random.uniform(-0.08, 0.08), 0])
            p.add_updater(lambda m, dt, v=velocity: m.shift(v * dt))
            particles.add(p)
        self.add(particles)

        # --- 2. THE TEXT ("Math is the bridge.") ---
        final_quote = Text("Math is the bridge.", color=TEXT_COLOR, font_size=40)
        underline = Line(LEFT, RIGHT, color=PRIMARY_COLOR, stroke_width=3)
        underline.match_width(final_quote).next_to(final_quote, DOWN, buff=0.2)
        
        # VGroup is fine here because both are vector objects
        quote_group = VGroup(final_quote, underline).move_to(ORIGIN)

        # --- 3. THE FINAL IMAGE & FRAMING ---
        try:
            # Using raw string for Windows path
            cat_image = ImageMobject(r"D:\manim\cat_sleeping.png")
            cat_image.height = 4.5
        except:
            # Fallback if image isn't found
            cat_image = RoundedRectangle(
                corner_radius=0.2, height=4.5, width=6.5, 
                color=GRAY, fill_opacity=0.1
            )

        # Create frames (Vector objects)
        inner_frame = SurroundingRectangle(cat_image, color=PRIMARY_COLOR, buff=0, stroke_width=3, corner_radius=0.1)
        outer_frame = SurroundingRectangle(cat_image, color=FRAME_COLOR, buff=0.15, stroke_width=2, corner_radius=0.2)

        # FIXED: Using Group instead of VGroup to combine ImageMobject and VMobjects
        final_image_group = Group(outer_frame, inner_frame, cat_image).move_to(ORIGIN)

        # --- 4. ANIMATION SEQUENCE ---

        # Phase 1: Typing-style reveal of the text
        self.play(
            AddTextLetterByLetter(final_quote),
            Create(underline),
            run_time=2.5
        )
        self.wait(1.5)

        # Phase 2: Smooth transition to the image
        self.play(
            quote_group.animate.to_edge(UP, buff=1.0).set_opacity(0),
            run_time=1.2
        )

        # Phase 3: Framed image reveal
        # We use FadeIn for the Group
        self.play(
            FadeIn(final_image_group, scale=1.05),
            run_time=2,
            rate_func=smooth
        )

        # Final Polish: Gentle pulse on the frame
        self.play(
            outer_frame.animate.scale(1.05).set_stroke(opacity=0.8),
            rate_func=there_and_back,
            run_time=2
        )

        self.wait(4)

