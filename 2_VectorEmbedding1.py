from manim import *
import numpy as np

# --- Absolute Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Light Pink
ACCENT_COLOR = "#be185d"       # Deep Pink
UI_GREY = "#94a3b8"            # Slate for borders
TEXT_DARK = "#1f2937"          # Professional Dark Grey
GRID_COLOR = "#e5e7eb"         # UI Separators
FAILURE_COLOR = "#ef4444"      # Red

# --- 1. Google Search Animation ---
class GoogleSearchCloudComputing(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        browser_canvas = RoundedRectangle(
            height=6.5, width=11, corner_radius=0.15,
            color=PRIMARY_COLOR, stroke_width=2,
            fill_color=WHITE, fill_opacity=1
        )
        header_divider = Line(
            start=browser_canvas.get_corner(UL) + DOWN * 0.8,
            end=browser_canvas.get_corner(UR) + DOWN * 0.8,
            color=GRID_COLOR, stroke_width=1.5
        )
        window_dots = VGroup(*[
            Dot(radius=0.07, color=c) for c in [ACCENT_COLOR, PRIMARY_COLOR, SECONDARY_COLOR]
        ]).arrange(RIGHT, buff=0.15).move_to(browser_canvas.get_corner(UL) + DR * 0.4)

        google_logo = Text("Google", font="serif", font_size=82, color=PRIMARY_COLOR, weight=NORMAL).shift(UP * 1.1)
        search_box = RoundedRectangle(height=0.8, width=7, corner_radius=0.4, color=PRIMARY_COLOR, stroke_width=2).next_to(google_logo, DOWN, buff=0.7)
        search_icon = VGroup(Circle(radius=0.1, color=PRIMARY_COLOR), Line(ORIGIN, DR * 0.08, color=PRIMARY_COLOR)).next_to(search_box.get_left(), RIGHT, buff=0.3)
        
        search_query = Text("Mount Everest", font="sans-serif", font_size=20, color=PRIMARY_COLOR).next_to(search_icon, RIGHT, buff=0.3).match_y(search_box)
        cursor = Line(UP * 0.25, DOWN * 0.25, color=PRIMARY_COLOR, stroke_width=2.5).next_to(search_icon, RIGHT, buff=0.3).match_y(search_box)

        # UI Buttons
        btn_config = {"height": 0.55, "width": 1.9, "corner_radius": 0.1, "fill_opacity": 1}
        search_btn = RoundedRectangle(color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, **btn_config)
        lucky_btn = RoundedRectangle(color=SECONDARY_COLOR, fill_color=SECONDARY_COLOR, **btn_config)
        footer_btns = VGroup(VGroup(search_btn, Text("Google Search", font_size=12, color=WHITE).move_to(search_btn)),
                             VGroup(lucky_btn, Text("I'm Feeling Lucky", font_size=12, color=PRIMARY_COLOR).move_to(lucky_btn))
                            ).arrange(RIGHT, buff=0.5).next_to(search_box, DOWN, buff=0.6)

        # ANIMATION (Total: ~28s)
        self.play(Create(browser_canvas), Create(header_divider), FadeIn(window_dots), run_time=2.5)
        self.play(Write(google_logo), run_time=2.5)
        self.wait(1)
        self.play(Create(search_box), FadeIn(search_icon), FadeIn(footer_btns, shift=UP*0.2), FadeIn(cursor), run_time=2)
        self.wait(2)
        
        cursor.add_updater(lambda m: m.next_to(search_query, RIGHT, buff=0.08))
        self.play(AddTextLetterByLetter(search_query), run_time=4.5, rate_func=linear)
        self.wait(1.5)
        cursor.remove_updater(cursor.updaters[0])
        
        self.play(search_btn.animate.scale(0.95), rate_func=there_and_back, run_time=0.5)
        self.play(Blink(cursor, run_time=6)) 
        self.wait(5)

# --- 2. 3D Neural Network & Vector Cloud ---
class FastAIInitiative3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = WHITE
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        title = Text("The First-Principles AI Gap", color=BLACK, font_size=32, weight=NORMAL)
        self.add_fixed_in_frame_mobjects(title)
        title.to_corner(UL, buff=0.5)

        def create_layer(nodes_count, z_offset, color):
            layer = VGroup()
            for i in range(nodes_count):
                node = Dot(point=[np.cos(TAU*i/nodes_count)*1.5, np.sin(TAU*i/nodes_count)*1.5, z_offset], radius=0.1, color=color)
                layer.add(node)
            return layer

        input_layer = create_layer(6, -2, "#94a3b8")
        hidden_layer = create_layer(8, 0, PRIMARY_COLOR)
        output_layer = create_layer(4, 2, PRIMARY_COLOR)
        connections = VGroup(*[Line(n1.get_center(), n2.get_center(), color=SECONDARY_COLOR, stroke_width=1) 
                               for l1, l2 in [(input_layer, hidden_layer), (hidden_layer, output_layer)] 
                               for i, n1 in enumerate(l1) for j, n2 in enumerate(l2) if (i+j)%2==0])

        neural_net = VGroup(input_layer, hidden_layer, output_layer, connections)

        # ANIMATION (Total: ~27s)
        self.begin_ambient_camera_rotation(rate=0.08)
        self.play(FadeIn(neural_net), run_time=3)
        
        info_text = Text("Isolated Model: Zero Context", font_size=18, color=TEXT_DARK)
        self.add_fixed_in_frame_mobjects(info_text)
        info_text.next_to(title, DOWN, buff=0.2).align_to(title, LEFT)
        self.play(Write(info_text), run_time=2.5)
        self.wait(4)

        vector_cloud = VGroup(*[Dot(point=[np.random.uniform(-3.5, 3.5) for _ in range(3)], radius=0.03, color=SECONDARY_COLOR) for _ in range(80)])
        success_text = Text("Solution: Semantic Vector Cloud", font_size=18, color=PRIMARY_COLOR)
        self.add_fixed_in_frame_mobjects(success_text)
        success_text.next_to(title, DOWN, buff=0.2).align_to(title, LEFT)

        self.play(FadeOut(info_text), Write(success_text), FadeIn(vector_cloud), run_time=3)
        self.wait(3)
        
        hits = VGroup(*[vector_cloud[i] for i in range(12)])
        self.play(hits.animate.set_color(PRIMARY_COLOR).scale(2.5), run_time=2)
        
        summary = Text("Semantic search provides the 'Fuel' for AI.", font_size=18, color=TEXT_DARK)
        self.add_fixed_in_frame_mobjects(summary)
        summary.to_edge(DOWN, buff=0.5)
        self.play(Write(summary), run_time=2)
        self.wait(7.5)

# --- 3. Keyword Search Checkmark ---
class KeywordSearchCheckmark(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = Text("Keyword Search = Exact Match", color=BLACK, weight=NORMAL).scale(0.8).to_edge(UP, buff=0.5)
        underline = Underline(title, color=GRID_COLOR)
        
        # UI Elements
        query_label = Text("Query:", color=TEXT_DARK, font_size=24).to_edge(LEFT, buff=1.5).shift(UP * 1.8)
        query_box = RoundedRectangle(corner_radius=0.1, height=0.7, width=4.5, color=GRID_COLOR)
        query_box.next_to(query_label, RIGHT, buff=0.3)
        query_text = Text("Everest", color=PRIMARY_COLOR, font_size=28).move_to(query_box)

        options_raw = ["A. Mount Everest is the highest mountain.", "B. Everest lies in the Himalayas.", 
                       "C. The tallest mountain on Earth.", "D. K2 is the second-highest mountain after Everest.", "E. Kilimanjaro is in Africa."]
        options_vgroup = VGroup(*[Text(opt, color=TEXT_DARK, font_size=22) for opt in options_raw]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 0.5)

        # ANIMATION (Total: ~29s)
        self.play(Write(title), Create(underline), run_time=2.5)
        self.play(FadeIn(query_label), Create(query_box), Write(query_text), run_time=2)
        self.play(LaggedStart(*[FadeIn(opt) for opt in options_vgroup], lag_ratio=0.3), run_time=4)
        self.wait(2)

        tick_a = Text("✔", color=PRIMARY_COLOR, font_size=24).next_to(options_vgroup[0], LEFT, buff=0.4)
        tick_b = Text("✔", color=PRIMARY_COLOR, font_size=24).next_to(options_vgroup[1], LEFT, buff=0.4)
        tick_d = Text("✔", color=PRIMARY_COLOR, font_size=24).next_to(options_vgroup[3], LEFT, buff=0.4)
        res1 = Text("Result: A, B, D", color=PRIMARY_COLOR, font_size=26).next_to(options_vgroup, DOWN, buff=0.8)

        self.play(FadeIn(tick_a), FadeIn(tick_b), FadeIn(tick_d), Write(res1), run_time=2)
        self.wait(3)

        new_query = Text("Mount Everest", color=PRIMARY_COLOR, font_size=28).move_to(query_box)
        res2 = Text("Result: A", color=PRIMARY_COLOR, font_size=26).next_to(options_vgroup, DOWN, buff=0.8)
        
        self.play(Transform(query_text, new_query), FadeOut(res1), FadeOut(tick_b), FadeOut(tick_d), run_time=2)
        self.play(Write(res2), run_time=1.5)
        
        exp = Text("Only option A contains the exact phrase 'Mount Everest'.", color=TEXT_DARK, font_size=18).next_to(res2, DOWN, buff=0.3)
        self.play(FadeIn(exp), run_time=2)
        self.wait(8)

# --- 4. Semantic Search Scene ---
class SemanticSearchScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = Text("Semantic Search = Context & Meaning", color=BLACK, weight=NORMAL).scale(0.8).to_edge(UP, buff=0.5)
        
        query_box = RoundedRectangle(corner_radius=0.1, height=0.7, width=4.5, color=PRIMARY_COLOR).shift(UP * 1.8)
        query_text = Text("Mount Everest", color=PRIMARY_COLOR, font_size=28).move_to(query_box)
        
        options = VGroup(*[Text(opt, color=TEXT_DARK, font_size=22) for opt in [
            "A. Mount Everest is the highest mountain.", "B. Everest lies in the Himalayas.", 
            "C. The tallest mountain on Earth.", "D. K2 is the second-highest mountain...", "E. Kilimanjaro..."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 0.5)

        # ANIMATION (Total: ~26s)
        self.play(Write(title), run_time=2)
        self.play(Create(query_box), Write(query_text), run_time=2)
        self.play(FadeIn(options, lag_ratio=0.2), run_time=3)
        self.wait(2)

        ticks = VGroup(*[Text("✔", color=PRIMARY_COLOR, font_size=24).next_to(options[i], LEFT, buff=0.4) for i in range(3)])
        res = Text("Result: A, B, C", color=PRIMARY_COLOR, font_size=26).next_to(options, DOWN, buff=0.8)
        
        self.play(FadeIn(ticks), Write(res), run_time=3)
        self.wait(2)
        
        exp = Text("Why? They all refer to the same concept/intent.", color=TEXT_DARK, font_size=18).next_to(res, DOWN, buff=0.3)
        self.play(FadeIn(exp), run_time=2)
        self.wait(10)

# --- 5. AI Understanding (Semantic Web) ---
class AIUnderstandingScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = Text("Semantic Search: Understanding Intent", color=BLACK, font_size=32).to_edge(UP, buff=0.5)

        words = ["Server", "Compute", "Cloud Hosting", "Provision a virtual machine", "Deploy infrastructure as code"]
        positions = [[-3, 1, 0], [0, 1.5, 0], [3, 1, 0], [-2, -1, 0], [2, -1, 0]]
        
        dots = VGroup(*[Dot(point=p, color=GRID_COLOR) for p in positions])
        labels = VGroup(*[Text(w, color=TEXT_DARK, font_size=18).next_to(d, UP, buff=0.2) for w, d in zip(words, dots)])
        lines = VGroup(*[Line(dots[i].get_center(), dots[(i+1)%len(dots)].get_center(), color=GRID_COLOR) for i in range(len(dots))])

        # ANIMATION (Total: ~28s)
        self.play(Write(title), run_time=2.5)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.4), run_time=4)
        self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=0.4), run_time=4)
        self.play(Create(lines), run_time=4)
        self.wait(1.5)
        
        self.play(lines.animate.set_color(PRIMARY_COLOR).set_stroke(width=4), 
                  dots.animate.set_color(PRIMARY_COLOR).scale(1.5), run_time=3)
        
        conc = Text("AI maps concepts, not just letters.", color=PRIMARY_COLOR, font_size=26).to_edge(DOWN, buff=1)
        self.play(Write(conc), run_time=2.5)
        self.wait(6.5)

# --- 6. Precise Routing ---
class PreciseRouting(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = Text("Semantic Intent Routing", color=BLACK, font_size=32).to_edge(UP, buff=0.5)
        
        # Simplified components for clarity
        router = RoundedRectangle(height=1.5, width=2.5, color=PRIMARY_COLOR).move_to(ORIGIN)
        label = Text("Semantic Router", font_size=18).move_to(router)
        
        # ANIMATION (Total: ~30s)
        self.play(Write(title), run_time=2)
        self.play(Create(router), Write(label), run_time=2.5)
        self.wait(1)

        scenarios = ["Cloud Storage?", "Password Reset?", "Sync Photos?"]
        for s in scenarios:
            query = Text(f"Query: {s}", font_size=20, color=PRIMARY_COLOR).to_edge(LEFT, buff=1)
            dot = Dot(color=PRIMARY_COLOR).move_to(query.get_right())
            self.play(FadeIn(query), run_time=1.5)
            self.play(dot.animate.move_to(router.get_left()), run_time=1.5)
            self.play(router.animate.scale(1.1), rate_func=there_and_back, run_time=0.5)
            self.play(FadeOut(dot), FadeOut(query), run_time=1)
            self.wait(1)
            
        footer = Text("Understanding intent ensures every query finds the right path.", font_size=18, color=PRIMARY_COLOR).to_edge(DOWN)
        self.play(FadeIn(footer), run_time=2.5)
        self.wait(10)

# --- 7. Keyword Failure (Mismatch Analysis) ---
class KeywordFailureScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = Text("Where Keyword Search Fails", color=BLACK, font_size=32).to_edge(UP, buff=0.7)
        
        query = Text('"How can we lower our monthly infrastructure spend?"', color=PRIMARY_COLOR, font_size=22).shift(UP * 1.5)
        
        box_a = RoundedRectangle(width=5, height=1.2, color=GRID_COLOR).shift(LEFT * 3 + DOWN * 0.5)
        text_a = Text("Reduce cloud costs\nthis quarter.", font_size=16).move_to(box_a)
        
        box_b = RoundedRectangle(width=5, height=1.2, color=GRID_COLOR).shift(RIGHT * 3 + DOWN * 0.5)
        text_b = Text("Infrastructure spending\nneeds to come down.", font_size=16).move_to(box_b)

        # ANIMATION (Total: ~27s)
        self.play(Write(title), run_time=2.5)
        self.play(FadeIn(query, shift=DOWN), run_time=2.5)
        self.wait(2)
        self.play(Create(box_a), Write(text_a), Create(box_b), Write(text_b), run_time=4)
        self.wait(3)
        
        unequal = MathTex(r"\neq", color=FAILURE_COLOR).scale(3).move_to(ORIGIN).shift(DOWN * 0.5)
        label = Text("No Keyword Overlap", color=FAILURE_COLOR, font_size=20).next_to(unequal, DOWN)
        
        self.play(Write(unequal), run_time=2)
        self.play(Write(label), run_time=2)
        self.wait(2)
        
        footer = Text("Keyword search sees words, not intent.", color=TEXT_DARK, font_size=16, slant=ITALIC).to_edge(DOWN)
        self.play(FadeIn(footer), run_time=2)
        self.wait(5)

# --- 8. Vector Representation ---
class CloudVectorRepresentation(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = Text("Contextual Vector Representation", color=BLACK, font_size=32).to_edge(UP, buff=0.7)

        rows = [
            {"t": '"cloud"', "v": "[ 0.21, -0.84, 1.32 ]", "c": TEXT_DARK},
            {"t": '"cloud computing"', "v": "[ 0.89, 0.12, -0.44 ]", "c": PRIMARY_COLOR},
            {"t": '"rain cloud"', "v": "[ -0.56, 0.98, 0.11 ]", "c": PRIMARY_COLOR},
        ]

        # ANIMATION (Total: ~28s)
        self.play(Write(title), run_time=2.5)
        self.wait(1.5)

        for i, row in enumerate(rows):
            txt = Text(row["t"], font_size=24, color=row["c"]).move_to([-4, 1 - i*1.2, 0], aligned_edge=LEFT)
            vec = Text(row["v"], font_size=22, color=row["c"]).move_to([1, 1 - i*1.2, 0], aligned_edge=LEFT)
            arrow = Arrow(txt.get_right(), vec.get_left(), color=GRID_COLOR)
            
            self.play(FadeIn(txt), GrowArrow(arrow), Write(vec), run_time=3.5)
            self.wait(1)

        summary = Text("The same word shifts its vector position based on context.", color=PRIMARY_COLOR, font_size=18).to_edge(DOWN, buff=1)
        self.play(Write(summary), run_time=3)
        self.wait(7.5)