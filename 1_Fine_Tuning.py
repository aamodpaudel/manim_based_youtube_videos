from manim import *
import numpy as np
import random

# ==========================================
# CONFIGURATION & THEME
# ==========================================
# Color Palette defined by user requirements
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (The main theme color)
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink (for background accents)
ACCENT_COLOR = "#be185d"       # darker shade of primary for emphasis
TEXT_COLOR = "#1f2937"         # Dark Grey/Black for high contrast text on white
GRID_COLOR = "#e5e7eb"         # Light grey for axes and grids

# Global Manim Configuration
config.background_color = WHITE
config.frame_width = 14
config.frame_height = 8

# ==========================================
# SCENE 1: TITLE CARD & INTRO (0:00–0:20)
# ==========================================
class Scene01_TitleCard(Scene):
    def construct(self):
        # Decorative background element
        bg_circle = Circle(radius=3.5, color=PRIMARY_COLOR, stroke_opacity=0.3, stroke_width=2)
        bg_circle.set_fill(SECONDARY_COLOR, opacity=0.4)

        # Title Text
        title = Text("Fine-Tuning a Computer Vision Model", color=PRIMARY_COLOR, font_size=42, weight=BOLD)
        subtitle = Text("A Pet Sentiment Classifier", color=TEXT_COLOR, font_size=32)
        subtitle.next_to(title, DOWN, buff=0.5)

        # Tagline
        tagline = Text("Explained using high-school mathematics.", color=GRAY, font_size=24, slant=ITALIC)
        tagline.next_to(subtitle, DOWN, buff=1.0)

        # Floating Math Symbols for atmosphere
        symbols = VGroup(
            MathTex(r"\nabla L", color=PRIMARY_COLOR).scale(0.8),
            MathTex(r"\sum", color=PRIMARY_COLOR).scale(0.8),
            MathTex(r"\int", color=PRIMARY_COLOR).scale(0.8),
            MathTex(r"\vec{x} \cdot \vec{w}", color=PRIMARY_COLOR).scale(0.8),
        )
        # Position symbols around the center
        positions = [UP*2.5 + LEFT*3, UP*2.5 + RIGHT*3, DOWN*2.5 + LEFT*3, DOWN*2.5 + RIGHT*3]
        for sym, pos in zip(symbols, positions):
            sym.move_to(pos)

        # Animations
        self.play(DrawBorderThenFill(bg_circle), run_time=2)
        self.play(
            Write(title),
            LaggedStart(*[FadeIn(s, shift=UP*0.5) for s in symbols], lag_ratio=0.2),
            run_time=1.5
        )
        self.play(FadeIn(subtitle, shift=UP*0.2))
        self.play(Write(tagline), run_time=1)
        
        self.wait(2)
        
        # Transition out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )


# ==========================================
# PART I: WHAT IS FINE-TUNING? (0:20–3:00)
# ==========================================

class Scene02_LearningAsGraph(Scene):
    def construct(self):
        # Section Title
        section_title = Text("Part I: What is Fine-Tuning?", color=PRIMARY_COLOR, font_size=36).to_edge(UP)
        self.play(Write(section_title))

        # 1. Coordinate Geometry (The Error Surface)
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 9, 2],
            x_length=7,
            y_length=5,
            axis_config={"color": TEXT_COLOR, "include_tip": True, "numbers_to_exclude": []},
        ).shift(DOWN * 0.5)
        axes.add_coordinates(font_size=20, color=GRAY)

        labels = axes.get_axis_labels(
            x_label=Tex("Weight value ($w$)", color=TEXT_COLOR), 
            y_label=Tex("Prediction Error ($E$)", color=TEXT_COLOR)
        )

        # The Error Curve (Parabola)
        error_curve = axes.plot(lambda x: x**2, color=PRIMARY_COLOR, stroke_width=4)
        
        self.play(Create(axes), Write(labels))
        self.play(Create(error_curve), run_time=1.5)

        # 2. Error as Distance & 3. Gradient Descent
        # Initial random weight
        initial_w = 2.5
        current_w = ValueTracker(initial_w)
        
        # The dot representing the model's current state
        model_dot = always_redraw(lambda: Dot(
            point=axes.coords_to_point(current_w.get_value(), current_w.get_value()**2),
            color=ACCENT_COLOR, radius=0.12
        ))

        # Visualizing Error as Distance (Vertical line to x-axis)
        error_line = always_redraw(lambda: Line(
            start=axes.coords_to_point(current_w.get_value(), 0),
            end=axes.coords_to_point(current_w.get_value(), current_w.get_value()**2),
            color=ACCENT_COLOR, stroke_opacity=0.5, stroke_width=3, dashed_stroke_config={"dash_length": 0.1}
        ))

        self.play(FadeIn(model_dot), Create(error_line))

        # Visualizing the Slope (Gradient)
        tangent_line = always_redraw(lambda: axes.get_tangent_line(
            current_w.get_value(), error_curve, length=3, color=GRAY, stroke_width=2
        ))
        
        slope_label = MathTex(r"\text{slope} = \frac{d(\text{error})}{d(\text{weight})}", color=TEXT_COLOR).to_corner(UR).shift(DOWN)
        
        self.play(Create(tangent_line))
        self.play(Write(slope_label))
        self.wait(1)

        # Animate Gradient Descent (Sliding down the curve)
        self.play(
            current_w.animate.set_value(0),
            run_time=4,
            rate_func=exponential_decay
        )
        
        # Goal state
        goal_text = Text("Goal: Lowest Point (Minimum Error)", color=PRIMARY_COLOR, font_size=24).next_to(model_dot, DOWN)
        self.play(Write(goal_text))
        self.wait(2)
        
        # Transition
        self.play(FadeOut(VGroup(axes, labels, error_curve, model_dot, error_line, tangent_line, slope_label, goal_text, section_title)))


# ==========================================
# PART II: PET SENTIMENT CLASSIFIER (3:00–7:30)
# ==========================================

class Scene03_ImageAsMatrix(Scene):
    def construct(self):
        section_title = Text("Part II: The Classifier Model", color=PRIMARY_COLOR, font_size=36).to_edge(UP)
        sub_title = Text("Input: Image as Numbers", color=TEXT_COLOR, font_size=28).next_to(section_title, DOWN)
        self.play(Write(section_title), Write(sub_title))

        # -------------------------------------------------
        # Requirement: Topic 3 Visualization (Image to Matrix)
        # -------------------------------------------------
        grid_size = 6
        square_size = 0.7
        
        image_grid = VGroup()
        matrix_values = []
        
        # Seed for reproducibility of colors/numbers
        np.random.seed(101)

        # Create the visual pixel grid
        for i in range(grid_size):
            row_values = []
            for j in range(grid_size):
                # Generate realistic pixel values (0-255), kept smaller for visual cleanliness
                val = np.random.randint(20, 220) 
                # Create color based on value (Darker primary color for higher values)
                opacity = val / 255.0 * 0.8 + 0.2 # Ensure minimum opacity
                color = interpolate_color(WHITE, PRIMARY_COLOR, opacity)
                
                square = Square(side_length=square_size, fill_color=color, fill_opacity=1, stroke_color=GRAY, stroke_width=1)
                square.move_to([j*square_size, -i*square_size, 0])
                image_grid.add(square)
                row_values.append(val)
            matrix_values.append(row_values)
        
        image_grid.center().shift(LEFT * 3.5)
        grid_label = Text("Pixel Grid (Visual)", color=TEXT_COLOR, font_size=20).next_to(image_grid, UP)

        # Create the corresponding numerical matrix
        matrix = IntegerMatrix(matrix_values, v_buff=0.7, h_buff=0.7, bracket_h_buff=0.1, bracket_v_buff=0.1).scale(0.6)
        matrix.set_color(TEXT_COLOR)
        matrix.get_brackets().set_color(PRIMARY_COLOR)
        matrix.move_to(image_grid.get_center()).shift(RIGHT * 7)
        matrix_label = Text("Matrix (Mathematical)", color=TEXT_COLOR, font_size=20).next_to(matrix, UP)

        # Transformation Arrow
        arrow = Arrow(image_grid.get_right(), matrix.get_left(), color=ACCENT_COLOR, stroke_width=4, buff=0.5)

        # Animation
        self.play(Create(image_grid), Write(grid_label), run_time=2)
        self.wait(0.5)
        self.play(GrowArrow(arrow))
        self.play(Create(matrix), Write(matrix_label), run_time=2)
        
        # Highlight a correspondence to make the point clear
        idx = 15 # Arbitrary index
        self.play(
            image_grid[idx].animate.set_stroke(YELLOW, 3),
            matrix.get_entries()[idx].animate.set_color(YELLOW).scale(1.2),
            run_time=1
        )
        self.wait(2)
        
        self.play(FadeOut(VGroup(image_grid, grid_label, matrix, matrix_label, arrow, section_title, sub_title)))


class Scene04_CNNConvolution(Scene):
    def construct(self):
        title = Text("Feature Extraction: CNN Filters", color=TEXT_COLOR, font_size=28).to_edge(UP)
        self.play(Write(title))

        # 1. Simplified Image Matrix (5x5)
        input_data = np.random.randint(0, 5, (5, 5))
        input_matrix = IntegerMatrix(input_data, v_buff=0.8, h_buff=0.8).scale(0.7).shift(LEFT*3)
        input_matrix.set_color(TEXT_COLOR)
        input_label = Text("Input Image Matrix", font_size=20, color=GRAY).next_to(input_matrix, UP)

        # 2. The Filter (Kernel) 3x3
        filter_data = [[1, 0, -1], [1, 0, -1], [1, 0, -1]] # Example vertical edge filter
        filter_matrix = IntegerMatrix(filter_data, v_buff=0.8, h_buff=0.8).scale(0.7).shift(RIGHT*1)
        filter_matrix.set_color(PRIMARY_COLOR)
        filter_label = Text("Filter (Kernel)", font_size=20, color=PRIMARY_COLOR).next_to(filter_matrix, UP)

        # Formula
        formula = MathTex(r"\text{Output} = \sum (\text{Image Patch} \times \text{Filter})", color=TEXT_COLOR).to_edge(DOWN, buff=1)
        formula[0][0:6].set_color(ACCENT_COLOR) # Output
        formula[0][8:18].set_color(GRAY) # Image Patch
        formula[0][19:25].set_color(PRIMARY_COLOR) # Filter

        self.play(Create(input_matrix), Write(input_label))
        self.play(Create(filter_matrix), Write(filter_label))
        self.play(Write(formula))

        # 3. Sliding Window Animation
        # Define the 3x3 patch area on the input matrix
        input_rows = input_matrix.get_rows()
        # Top left corner of 3x3
        start_corner = input_rows[0][0].get_center() + UP*0.3 + LEFT*0.3
        # Bottom right corner of 3x3
        end_corner = input_rows[2][2].get_center() + DOWN*0.3 + RIGHT*0.3
        
        sliding_box = Rectangle(width=end_corner[0]-start_corner[0], height=start_corner[1]-end_corner[1], color=PRIMARY_COLOR)
        sliding_box.move_to((start_corner + end_corner) / 2)

        self.play(Create(sliding_box))
        self.wait(0.5)

        # Animate sliding one step right
        self.play(sliding_box.animate.shift(RIGHT * (input_rows[0][1].get_center()[0] - input_rows[0][0].get_center()[0])), run_time=1)
        self.wait(0.5)
        # Animate sliding one step down
        self.play(sliding_box.animate.shift(DOWN * (input_rows[0][0].get_center()[1] - input_rows[1][0].get_center()[1])), run_time=1)
        self.wait(1)
        
        desc = Text("Basic Algebra: Detects edges, textures, shapes.", color=ACCENT_COLOR, font_size=24).next_to(formula, UP)
        self.play(Write(desc))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class Scene05_ViTAndAttention(Scene):
    def construct(self):
        title = Text("Feature Extraction: Vision Transformer Patches", color=TEXT_COLOR, font_size=28).to_edge(UP)
        self.play(Write(title))

        # 1. Image to Patches
        image_square = Square(side_length=4, color=GRAY, fill_color=SECONDARY_COLOR, fill_opacity=0.5).shift(LEFT*4)
        image_label = Text("Image", font_size=20, color=GRAY).next_to(image_square, UP)

        self.play(Create(image_square), Write(image_label))

        # Divide into 2x2 patches
        patches = VGroup()
        for i in range(2):
            for j in range(2):
                patch = Square(side_length=2, color=PRIMARY_COLOR, stroke_width=2).move_to(
                    image_square.get_corner(UL) + RIGHT*(j*2 + 1) + DOWN*(i*2 + 1)
                )
                patches.add(patch)
        
        self.play(Create(patches), run_time=1.5)
        
        # 2. Patches to Vectors
        vector_group = VGroup()
        arrows = VGroup()
        
        for i, patch in enumerate(patches):
            # Representative vector matrix
            vec = Matrix([[f"p_{i+1}"], ["..."]], v_buff=0.4,bracket_h_buff=0.1, bracket_v_buff=0.1).scale(0.6)
            vec.set_color(TEXT_COLOR)
            vec.get_brackets().set_color(PRIMARY_COLOR)
            
            # Position vectors in a column to the right
            vec.move_to(RIGHT*0 + UP*(1.5 - i*1.5))
            vector_group.add(vec)
            
            # Arrow from patch to vector
            arrow = Arrow(patch.get_right(), vec.get_left(), color=GRAY, buff=0.2, stroke_width=2)
            arrows.add(arrow)

        vector_label = Text("Patch Vectors", font_size=20, color=TEXT_COLOR).next_to(vector_group, UP)

        self.play(GrowFromCenter(vector_group[0]), GrowArrow(arrows[0]))
        self.play(GrowFromCenter(vector_group[1]), GrowArrow(arrows[1]))
        self.play(GrowFromCenter(vector_group[2]), GrowArrow(arrows[2]))
        self.play(GrowFromCenter(vector_group[3]), GrowArrow(arrows[3]), Write(vector_label))
        self.wait(1)

        # 3. Attention (Dot Product)
        # Focus on two vectors
        self.play(
            FadeOut(image_square), FadeOut(patches), FadeOut(image_label), FadeOut(arrows),
            vector_group[2:].animate.set_opacity(0.2)
        )

        vec_a = vector_group[0]
        vec_b = vector_group[1]
        
        dot_product_title = Text("Compare Patches: Dot Product", color=PRIMARY_COLOR, font_size=24).shift(RIGHT*4 + UP*2)
        
        # Math formulas
        formula_vec = MathTex(r"\vec{a} \cdot \vec{b}", color=TEXT_COLOR).next_to(dot_product_title, DOWN, buff=0.5)
        formula_vec[0][0:2].set_color(PRIMARY_COLOR) # vec a
        formula_vec[0][3:5].set_color(ACCENT_COLOR) # vec b
        
        formula_expanded = MathTex(
            r"= (a_1 \times b_1) + (a_2 \times b_2) + \dots", color=TEXT_COLOR
        ).next_to(formula_vec, DOWN)

        interpretation = Text("Larger Value = Stronger Similarity", color=ACCENT_COLOR, font_size=20).next_to(formula_expanded, DOWN, buff=0.5)

        self.play(Write(dot_product_title))
        self.play(
            vec_a.animate.set_color(PRIMARY_COLOR),
            vec_b.animate.set_color(ACCENT_COLOR),
            Write(formula_vec)
        )
        self.play(Write(formula_expanded))
        self.play(Write(interpretation))
        self.wait(2)

        # 4. Weighted Average Formula
        attention_formula = MathTex(
            r"\text{Attention} = \frac{\sum (\text{weight} \times \text{patch})}{\sum \text{weights}}",
            color=TEXT_COLOR
        ).shift(DOWN*2.5)
        attention_formula[0][0:9].set_color(PRIMARY_COLOR)
        
        attention_desc = Text("A weighted mean of features.", color=GRAY, font_size=20).next_to(attention_formula, DOWN)

        self.play(Write(attention_formula))
        self.play(Write(attention_desc))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


# ==========================================
# PART III: FINE-TUNING THIS MODEL (7:30–10:00)
# ==========================================

class Scene06_ClassificationLayer(Scene):
    def construct(self):
        section_title = Text("Part III: Fine-Tuning & Classification", color=PRIMARY_COLOR, font_size=36).to_edge(UP)
        self.play(Write(section_title))
        
        sub_title = Text("The Emotion Classification Layer", color=TEXT_COLOR, font_size=28).next_to(section_title, DOWN)
        self.play(Write(sub_title))

        # -------------------------------------------------
        # Requirement: Topic 2 Visualization (Neural Network)
        # -------------------------------------------------
        # Define layer sizes: Input features -> Hidden -> Output (Emotions)
        layer_sizes = [4, 3, 2] 
        
        neurons = VGroup()
        edges = VGroup()
        
        # Positioning parameters
        start_x = -3
        layer_spacing = 3
        
        for i, size in enumerate(layer_sizes):
            layer_group = VGroup()
            x = start_x + i * layer_spacing
            # Center layers vertically
            start_y = (size - 1) * 0.6 
            
            for j in range(size):
                y = start_y - j * 1.2
                # Neurons: White fill, Primary outline
                neuron = Circle(radius=0.3, color=PRIMARY_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2)
                neuron.move_to([x, y, 0])
                layer_group.add(neuron)
            neurons.add(layer_group)
            
        # Create edges (dense connections)
        for i in range(len(layer_sizes) - 1):
            for n1 in neurons[i]:
                for n2 in neurons[i+1]:
                    edge = Line(n1.get_right(), n2.get_left(), color=SECONDARY_COLOR, stroke_width=1)
                    edges.add(edge, to_back=True) # Put edges behind neurons

        # Labels
        labels = VGroup(
            Text("Extracted Features", font_size=16, color=GRAY).next_to(neurons[0], DOWN),
            Text("Hidden Layer", font_size=16, color=GRAY).next_to(neurons[1], DOWN),
            Text("Output (Logits $z$)", font_size=16, color=PRIMARY_COLOR).next_to(neurons[2], DOWN),
        )

        # Center the whole network
        network_group = VGroup(neurons, edges, labels).center()
        
        self.play(
            LaggedStart(*[Create(layer) for layer in neurons], lag_ratio=0.3),
            ShowPassingFlash(edges.copy().set_color(PRIMARY_COLOR), time_width=0.5, run_time=2),
            Create(edges),
            run_time=3
        )
        self.play(Write(labels))

        # Linear Algebra Formula
        formula = MathTex(r"z = w_1x_1 + w_2x_2 + \dots + b", color=TEXT_COLOR).to_edge(DOWN, buff=1.5)
        formula_desc = Text("Standard Linear Equation (like y = mx + c)", color=GRAY, font_size=20).next_to(formula, DOWN)
        
        self.play(Write(formula))
        self.play(Write(formula_desc))
        self.wait(2)

        # Transition to Softmax: Keep only the output layer and the formula
        self.play(
            FadeOut(neurons[0]), FadeOut(neurons[1]), FadeOut(edges), 
            FadeOut(labels[0]), FadeOut(labels[1]), FadeOut(sub_title),
            neurons[2].animate.center().shift(LEFT*3),
            labels[2].animate.next_to(neurons[2].center().shift(LEFT*3), DOWN),
            formula.animate.shift(UP*1),
            FadeOut(formula_desc)
        )
        self.wait(1)


class Scene07_SoftmaxAndLoss(Scene):
    def construct(self):
        # Keep section title from previous scene conceptually
        section_title = Text("Part III: Fine-Tuning & Classification", color=PRIMARY_COLOR, font_size=36).to_edge(UP)
        self.add(section_title)

        # Recreate output nodes from previous scene for continuity
        output_nodes = VGroup(
            Circle(radius=0.3, color=PRIMARY_COLOR, fill_color=WHITE, fill_opacity=1),
            Circle(radius=0.3, color=PRIMARY_COLOR, fill_color=WHITE, fill_opacity=1)
        ).arrange(DOWN, buff=0.6).shift(LEFT*3)
        
        node_labels = VGroup(
            MathTex("z_1", color=TEXT_COLOR).move_to(output_nodes[0]),
            MathTex("z_2", color=TEXT_COLOR).move_to(output_nodes[1])
        )
        self.add(output_nodes, node_labels)

        # 1. Softmax
        softmax_title = Text("Convert to Probabilities: Softmax", color=TEXT_COLOR, font_size=24).next_to(output_nodes, UP, buff=1)
        self.play(Write(softmax_title))

        softmax_formula = MathTex(
            r"P_i = \frac{e^{z_i}}{\sum e^{z_j}}", color=PRIMARY_COLOR
        ).next_to(output_nodes, RIGHT, buff=2)

        self.play(Write(softmax_formula))

        # Show probabilities resulting
        arrow_top = Arrow(output_nodes[0].get_right(), output_nodes[0].get_right()+RIGHT*1.5, color=GRAY)
        arrow_bot = Arrow(output_nodes[1].get_right(), output_nodes[1].get_right()+RIGHT*1.5, color=GRAY)
        
        prob_top = Text("P(Happy) = 0.70", color=ACCENT_COLOR, font_size=20).next_to(arrow_top, RIGHT)
        prob_bot = Text("P(Sad)   = 0.30", color=GRAY, font_size=20).next_to(arrow_bot, RIGHT)

        self.play(GrowArrow(arrow_top), Write(prob_top))
        self.play(GrowArrow(arrow_bot), Write(prob_bot))
        self.wait(1)

        # 2. Loss and Fine-Tuning
        loss_title = Text("Compare & Adjust: Loss Function", color=TEXT_COLOR, font_size=24).to_edge(DOWN, buff=2.5)
        self.play(Write(loss_title))

        # Assume true label is 'Happy'
        true_label_txt = Text("True Label: Happy (1.0)", color=TEXT_COLOR, font_size=20).next_to(loss_title, DOWN)
        self.play(Write(true_label_txt))

        # Simplified Loss Formula (MSE style for visual clarity, though Cross-Entropy is usual)
        loss_formula = MathTex(r"\text{Loss} = (\text{Prediction} - \text{Actual})^2", color=PRIMARY_COLOR, font_size=30)
        loss_formula.next_to(true_label_txt, DOWN)
        
        loss_example = MathTex(r"\text{Loss} \approx (0.70 - 1.0)^2 = (-0.3)^2 = 0.09", color=ACCENT_COLOR, font_size=30)
        loss_example.next_to(loss_formula, DOWN)

        self.play(Write(loss_formula))
        self.play(Write(loss_example))
        self.wait(1)

        # Visualizing "Adjusting Weights"
        fine_tune_text = Text("Fine-Tuning: Adjust weights using derivatives to reduce Loss.", color=PRIMARY_COLOR, font_size=24,slant=ITALIC)
        fine_tune_text.to_edge(DOWN)
        
        # Animate the output nodes pulsing to show adjustment
        self.play(
            Write(fine_tune_text),
            output_nodes.animate.set_stroke(width=6, color=ACCENT_COLOR).set_fill(SECONDARY_COLOR),
            run_time=1.5,
            rate_func=there_and_back
        )
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class Scene08_Summary3D(ThreeDScene):
    def construct(self):
        # Title
        title = Text("Why it Matters: Better Clustering", color=PRIMARY_COLOR, font_size=36)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP)

        # 3D Axes
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4], x_length=8, y_length=8, z_length=8)
        axes.set_color(GRAY)
        
        # Labels for axes
        lab_x = axes.get_x_axis_label("Edge Feat.")
        lab_y = axes.get_y_axis_label("Texture Feat.")
        lab_z = axes.get_z_axis_label("Shape Feat.")
        axis_labels = VGroup(lab_x, lab_y, lab_z).set_color(GRAY).scale(0.7)

        # Data Points - State 1: Overlapping (Before Fine-tuning)
        np.random.seed(42)
        
        # Happy dogs (Primary color) - loosely centered
        happy_points_start = VGroup(*[
            Dot3D(point=[np.random.normal(0.5, 1), np.random.normal(0.5, 1), np.random.normal(0.5, 1)], color=PRIMARY_COLOR, radius=0.1) 
            for _ in range(20)
        ])
        # Sad dogs (Gray color) - loosely centered, overlapping
        sad_points_start = VGroup(*[
            Dot3D(point=[np.random.normal(-0.5, 1), np.random.normal(-0.5, 1), np.random.normal(-0.5, 1)], color=GRAY, radius=0.1) 
            for _ in range(20)
        ])
        
        label_before = Text("Before Fine-Tuning (Overlapping)", color=TEXT_COLOR, font_size=24)
        self.add_fixed_in_frame_mobjects(label_before)
        label_before.to_corner(UL).shift(DOWN)

        # Set initial camera view
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        self.play(Create(axes), Write(axis_labels))
        self.play(GrowFromCenter(happy_points_start), GrowFromCenter(sad_points_start))
        self.wait(1)

        # Data Points - State 2: Separated (After Fine-tuning)
        # Happy dogs move to positive quadrant
        happy_points_end = VGroup(*[
            Dot3D(point=[np.random.normal(2, 0.5), np.random.normal(2, 0.5), np.random.normal(2, 0.5)], color=PRIMARY_COLOR, radius=0.1) 
            for _ in range(20)
        ])
        # Sad dogs move to negative quadrant
        sad_points_end = VGroup(*[
            Dot3D(point=[np.random.normal(-2, 0.5), np.random.normal(-2, 0.5), np.random.normal(-2, 0.5)], color=GRAY, radius=0.1) 
            for _ in range(20)
        ])

        label_after = Text("After Fine-Tuning (Separated)", color=PRIMARY_COLOR, font_size=24)
        self.add_fixed_in_frame_mobjects(label_after)
        label_after.move_to(label_before)

        # Animate transition and camera rotation simultaneously
        self.play(
            Transform(happy_points_start, happy_points_end),
            Transform(sad_points_start, sad_points_end),
            Transform(label_before, label_after),
            Rotate(axes, angle=2*PI, axis=UP, about_point=ORIGIN, rate_func=smooth), # Rotate scene instead of camera for smoother control here
            run_time=4
        )

        # Add a visual decision boundary plane
        boundary_plane = Surface(
            lambda u, v: np.array([u, v, -u-v]), # Plane passing near origin roughly separating the clusters
            u_range=[-2, 2], v_range=[-2, 2],
            checkerboard_colors=[SECONDARY_COLOR, SECONDARY_COLOR],
            fill_opacity=0.3, stroke_color=ACCENT_COLOR, stroke_width=1
        )
        
        self.play(Create(boundary_plane), run_time=2)
        self.wait(2)


# ==========================================
# FINAL SCENE: SUMMARY TABLE
# ==========================================
class Scene09_FinalSummary(Scene):
    def construct(self):
        title = Text("Concept Summary", color=PRIMARY_COLOR, font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(title))

        # Data for the table
        data = [
            ["Concept", "Mathematical Tool"],
            ["Learning Process", "Coordinate Geometry & Graphs"],
            ["Reducing Error", "Calculus (Derivatives/Slopes)"],
            ["Image Representation", "Matrices (2D Grids of Numbers)"],
            ["Feature Detection (CNN)", "Linear Algebra (Convolution)"],
            ["Patch Similarity (ViT)", "Vectors & Dot Products"],
            ["Attention Mechanism", "Weighted Averages (Statistics)"],
            ["Final Classification", "Probability (Softmax Function)"],
        ]

        # Create the table structure using VGroup and text
        table_group = VGroup()
        row_height = 0.7
        col_widths = [5, 7]
        start_y = 2.5

        for i, row in enumerate(data):
            # Header style vs Content style
            color = PRIMARY_COLOR if i == 0 else TEXT_COLOR
            weight = BOLD if i == 0 else NORMAL
            
            # Concept Column
            t1 = Text(row[0], color=color, font_size=22, weight=weight)
            t1.move_to(UP * (start_y - i*row_height) + LEFT * (col_widths[1]/2))
            
            # Math Tool Column
            t2 = Text(row[1], color=color if i==0 else GRAY, font_size=22, weight=weight)
            t2.move_to(UP * (start_y - i*row_height) + RIGHT * (col_widths[0]/2))
            
            row_group = VGroup(t1, t2)
            table_group.add(row_group)
            
            # Add divider line below headers
            if i == 0:
                line = Line(LEFT*6, RIGHT*6, color=PRIMARY_COLOR, stroke_width=2)
                line.next_to(row_group, DOWN, buff=0.1)
                table_group.add(line)

        table_group.center().shift(DOWN*0.5)

        # Animate table creation row by row
        for item in table_group:
            self.play(FadeIn(item, shift=UP*0.2), run_time=0.3)
        
        self.wait(3)
        
        # Final End Screen
        self.play(FadeOut(table_group), FadeOut(title))
        
        end_text = Text("Thanks for watching!", color=PRIMARY_COLOR, font_size=48)
        sub_end = Text("Go build something awesome.", color=GRAY, font_size=24, slant=ITALIC).next_to(end_text, DOWN)
        
        self.play(Write(end_text), FadeIn(sub_end))
        self.wait(3)