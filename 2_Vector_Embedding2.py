from manim import *
import numpy as np

# --- Configuration & Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink
ACCENT_COLOR = "#be185d"       # Darker shade
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
GRID_COLOR = "#e5e7eb"         # Light grey
UNMATCHED_COLOR = "#94a3b8"   # Gray for lower scores

class VectorEmbeddingScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- 1. TITLE SECTION ---
        title = Text("How AI Understands Meaning", color=BLACK, font_size=32, weight=NORMAL)
        title.to_edge(UP, buff=0.7)

        # --- 2. INPUT DATA BLOCK ---
        input_box = RoundedRectangle(corner_radius=0.1, width=3.8, height=2.2, color=TEXT_COLOR)
        input_label = Text("Information Source", color=TEXT_COLOR, font_size=18).next_to(input_box, UP, buff=0.2)
        text_data_2 = Text('"Reduce Cloud Costs"', color=TEXT_COLOR, font_size=16)
        inputs_vgroup = VGroup(Text('Textual Input', color=TEXT_COLOR, font_size=16), text_data_2).arrange(DOWN, buff=0.4).move_to(input_box.get_center())
        input_section = VGroup(input_box, input_label, inputs_vgroup).to_edge(LEFT, buff=0.6)

        # --- 3. THE EMBEDDING MODEL ---
        model_box = Rectangle(width=2.8, height=3.2, color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=0.1)
        model_label = Text("Vector\nEmbedding\nModel", color=PRIMARY_COLOR, font_size=20, weight=NORMAL).move_to(model_box.get_center())
        model_section = VGroup(model_box, model_label)

        # --- 4. THE NUMERICAL VECTOR ---
        vector_math = MathTex(r"\begin{bmatrix} 0.12 \\ -0.85 \\ 0.43 \\ \vdots \\ 0.91 \end{bmatrix}", color=TEXT_COLOR).scale(0.8)
        vector_box = RoundedRectangle(corner_radius=0.1, width=2.2, height=3.5, color=PRIMARY_COLOR)
        vector_label = Text("Vector", color=PRIMARY_COLOR, font_size=18).next_to(vector_box, UP, buff=0.2)
        vector_section = VGroup(vector_box, vector_label, vector_math).to_edge(RIGHT, buff=0.6)

        arrow1 = Arrow(input_box.get_right(), model_box.get_left(), color=GRID_COLOR, buff=0.1)
        arrow2 = Arrow(model_box.get_right(), vector_box.get_left(), color=PRIMARY_COLOR, buff=0.1)

        # --- ANIMATION SEQUENCE (Total ~28s) ---
        self.play(Write(title, run_time=2.5))
        self.play(Create(input_section), run_time=2)
        self.play(Create(model_section), GrowArrow(arrow1), run_time=2.5)
        self.play(GrowArrow(arrow2), FadeIn(vector_section, shift=LEFT), run_time=2.5)
        self.wait(4)

        self.play(FadeOut(input_section), FadeOut(model_section), FadeOut(arrow1), FadeOut(arrow2), FadeOut(vector_section), run_time=2)

        # Phase 2: The Semantic Map
        coord_grid = NumberPlane(x_range=[-5, 5, 1], y_range=[-3, 3, 1], background_line_style={"stroke_opacity": 0.3, "stroke_color": GRID_COLOR})
        node_cost = Dot(point=[-1.5, 0.5, 0], color=PRIMARY_COLOR, radius=0.12)
        label_cost = Text("Cloud Costs", font_size=18, color=TEXT_COLOR).next_to(node_cost, UP, buff=0.15)
        node_spending = Dot(point=[-1.0, -0.8, 0], color=PRIMARY_COLOR, radius=0.12)
        label_spending = Text("Bills & Spending", font_size=18, color=TEXT_COLOR).next_to(node_spending, DOWN, buff=0.15)
        rel_line = Line(node_cost.get_center(), node_spending.get_center(), color=PRIMARY_COLOR, stroke_width=4)
        
        self.play(Create(coord_grid, run_time=2))
        self.play(LaggedStart(Create(node_cost), Write(label_cost), Create(node_spending), Write(label_spending), lag_ratio=0.5, run_time=3))
        self.play(Create(rel_line), run_time=1.5)
        
        conclusion = Text("Mapping ideas, not memorizing words.", color=PRIMARY_COLOR, font_size=24).to_edge(DOWN, buff=0.6)
        bg_rect = SurroundingRectangle(conclusion, color=SECONDARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=1, buff=0.2)
        
        self.play(FadeIn(bg_rect), Write(conclusion, run_time=2.5))
        self.wait(5)

class SemanticMathAnimations(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Scene 1: Cosine Similarity (Total ~30s) ---
        title_1 = Text("Semantic Understanding: Cosine Similarity", color=BLACK, font_size=32, weight=NORMAL).to_edge(UP, buff=0.5)
        text_a = VGroup(MathTex(r"\vec{A}:", color=PRIMARY_COLOR, font_size=24), Text('"Reduce cloud costs."', color=TEXT_COLOR, font_size=18)).arrange(RIGHT)
        text_b = VGroup(MathTex(r"\vec{B}:", color=PRIMARY_COLOR, font_size=24), Text('"Optimize infrastructure spending."', color=TEXT_COLOR, font_size=18)).arrange(RIGHT)
        sentences = VGroup(text_a, text_b).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT, buff=0.8).shift(UP * 1.5)

        plane = NumberPlane(x_range=[-0.5, 4, 1], y_range=[-0.5, 4, 1], background_line_style={"stroke_color": GRID_COLOR}).scale(0.8).shift(DOWN * 0.5 + RIGHT * 1.5)
        vec_a = Arrow(plane.coords_to_point(0,0), plane.coords_to_point(3.0, 0.8), color=PRIMARY_COLOR, buff=0)
        vec_b = Arrow(plane.coords_to_point(0,0), plane.coords_to_point(2.2, 2.2), color=ACCENT_COLOR, buff=0)
        theta_arc = Arc(radius=0.7, start_angle=np.arctan2(0.8, 3.0), angle=np.arctan2(2.2, 2.2)-np.arctan2(0.8, 3.0), arc_center=plane.coords_to_point(0,0), color=TEXT_COLOR)

        self.play(Write(title_1, run_time=2.5))
        self.play(FadeIn(sentences, shift=RIGHT, run_time=3))
        self.play(Create(plane), GrowArrow(vec_a), GrowArrow(vec_b), run_time=4)
        self.play(Create(theta_arc), Write(MathTex(r"\theta", color=TEXT_COLOR).move_to(theta_arc).shift(RIGHT*0.3)), run_time=2)
        self.play(Write(MathTex(r"\cos(\theta) = 0.94", color=PRIMARY_COLOR).next_to(sentences, DOWN, buff=1), run_time=2.5))
        self.wait(5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=2)

        # --- Scene 2: Dot Product Calculation ---
        title_2 = Text("Mathematical Calculation: Dot Product", color=BLACK, font_size=32, weight=NORMAL).to_edge(UP, buff=0.5)
        vec_block = VGroup(MathTex(r"\vec{v}_A = [0.80, \ 0.50]", color=PRIMARY_COLOR), MathTex(r"\vec{v}_B = [0.75, \ 0.48]", color=TEXT_COLOR)).arrange(RIGHT, buff=1.5).shift(UP * 1.5)
        calc = VGroup(MathTex(r"\vec{v}_A \cdot \vec{v}_B = (0.80 \times 0.75) + (0.50 \times 0.48)"), MathTex(r"= 0.60 + 0.24"), MathTex(r"\text{Score} = 0.84")).arrange(DOWN, buff=0.5).shift(DOWN * 0.5)

        self.play(Write(title_2, run_time=2.5))
        self.play(FadeIn(vec_block, run_time=2.5))
        self.play(Write(calc[0], run_time=2.5))
        self.play(Write(calc[1], run_time=2))
        self.play(Write(calc[2], run_time=2))
        self.play(SurroundingRectangle(calc[2], color=PRIMARY_COLOR), run_time=1.5)
        self.wait(6)

class NumericalSimilarityMapping(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # --- Section 1: Table (Total ~28s) ---
        title = Text("Query: Mount Everest", color=BLACK, weight=NORMAL).scale(0.8).to_edge(UP, buff=0.5)
        table = Table([["Mount Washington", "0.89"], ["Nepal", "0.72"], ["Pacific Ocean", "0.31"], ["Tokyo", "0.14"]], col_labels=[Text("Option"), Text("Score")], include_outer_lines=True).scale(0.5).next_to(title, DOWN)
        
        self.play(Write(title, run_time=2))
        self.play(Create(table.get_horizontal_lines()), Create(table.get_vertical_lines()), run_time=3)
        self.play(Write(table.get_labels()), run_time=2)
        for row in table.get_rows()[1:]:
            self.play(FadeIn(row, shift=UP*0.2), run_time=1.5)
        self.wait(5)

        self.play(FadeOut(table), FadeOut(title), run_time=2)

        # --- Section 2: Spatial Graph ---
        graph_title = Text("Semantic Vector Proximity", color=BLACK, weight=NORMAL).scale(0.8).to_edge(UP, buff=0.5)
        everest_dot = Dot(point=ORIGIN, color=PRIMARY_COLOR, radius=0.15)
        
        self.play(Write(graph_title, run_time=2.5))
        self.play(Create(everest_dot), Write(Text("Mount Everest", font_size=24, color=PRIMARY_COLOR).next_to(everest_dot, UP)), run_time=2)
        
        points = [["Mount Washington", RIGHT*2, PRIMARY_COLOR], ["Nepal", LEFT*2.5 + UP*1.5, UNMATCHED_COLOR]]
        for pt in points:
            dot = Dot(point=pt[1], color=pt[2])
            line = Line(everest_dot.get_center(), dot.get_center(), color=pt[2], buff=0.1)
            self.play(Create(line), FadeIn(dot), Write(Text(pt[0], font_size=20, color=pt[2]).next_to(dot, DR)), run_time=3)
        
        self.wait(7)

class SemanticTextSimilarity(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # --- Total ~27s ---
        query_label = Text("Input Query:", color=BLACK, font_size=24, weight=NORMAL).to_edge(UP, buff=0.4)
        query_text = Text('"I dream of climbing mount Everest once in my lifetime."', color=PRIMARY_COLOR, font_size=24).next_to(query_label, DOWN)

        table_content = [["Mountaineering is a professional career...", "0.72"], ["We teach people how to climb mountain...", "0.94"]]
        mobjects = [[Paragraph(row[0], color=TEXT_COLOR, font_size=32).set_width(8.5), Text(row[1], color=PRIMARY_COLOR if i==1 else UNMATCHED_COLOR, font_size=36)] for i, row in enumerate(table_content)]
        sim_table = MobjectTable(mobjects, col_labels=[Text("Match Options"), Text("Score")], include_outer_lines=True).next_to(query_text, DOWN, buff=0.5)

        self.play(FadeIn(query_label, run_time=2))
        self.play(Write(query_text, run_time=3.5))
        self.wait(2)
        self.play(Create(sim_table.get_horizontal_lines()), Create(sim_table.get_vertical_lines()), FadeIn(sim_table.get_labels()), run_time=4)
        
        for i, row in enumerate(sim_table.get_rows()[1:]):
            self.play(FadeIn(row, shift=RIGHT*0.4, run_time=2.5))
            if i == 1: self.play(row.animate.set_background_stroke(color=PRIMARY_COLOR, width=2), run_time=1.5)

        self.play(FadeIn(Text("Similarity is calculated via Cosine Similarity.", color=UNMATCHED_COLOR, font_size=16).to_edge(DOWN)), run_time=2)
        self.wait(8)

class SemanticSimilarityRephrased(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # --- Total ~27s ---
        query_label = Text("Input Query (Rephrased):", color=BLACK, font_size=24, weight=NORMAL).to_edge(UP, buff=0.4)
        query_text = Text('"I want to learn mountain climbing to reach Everest"', color=PRIMARY_COLOR, font_size=24).next_to(query_label, DOWN)

        table_content = [["Mountaineering is a professional career...", "0.70"], ["We teach people how to climb mountain...", "0.96"]]
        mobjects = [[Paragraph(row[0], color=TEXT_COLOR, font_size=32).set_width(8.5), Text(row[1], color=PRIMARY_COLOR if i==1 else UNMATCHED_COLOR, font_size=36)] for i, row in enumerate(table_content)]
        sim_table = MobjectTable(mobjects, col_labels=[Text("Match Options"), Text("Score")], include_outer_lines=True).next_to(query_text, DOWN, buff=0.6)

        self.play(FadeIn(query_label, run_time=2))
        self.play(Write(query_text, run_time=3))
        self.wait(2)
        self.play(Create(sim_table.get_horizontal_lines()), Create(sim_table.get_vertical_lines()), FadeIn(sim_table.get_labels()), run_time=4)
        
        for i, row in enumerate(sim_table.get_rows()[1:]):
            self.play(FadeIn(row, shift=RIGHT*0.4, run_time=2.5))
            if i == 1: self.play(row.animate.set_background_stroke(color=PRIMARY_COLOR, width=2), run_time=1.5)

        footer = Text("Even with rephrasing, the semantic intent yields high scores.", color=UNMATCHED_COLOR, font_size=14).to_edge(DOWN)
        self.play(FadeIn(footer, run_time=2.5))
        self.wait(8)