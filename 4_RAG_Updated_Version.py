from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Highlights, Numbers)
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # Black text for white background
ICON_BASE_COLOR = "#ec5599"    # Dark Grey (Change this to update all icons!)
BACKGROUND_COLOR = WHITE       # White background
LIGHT_PINK = "#fbcfe8"         # Solid Light Pink for Client

class RAGArchitectureScene(Scene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers ---

        def get_client_icon():
            # Proportional User Icon with larger head
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            
            body = AnnularSector(
                inner_radius=0, 
                outer_radius=0.5, 
                start_angle=PI, 
                angle=-PI, 
                color=LIGHT_PINK, 
                fill_opacity=1
            )
            body.stretch(1.2, dim=1) 
            body.shift(DOWN * 0.15)
            
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.5)
            spokes = VGroup()
            nodes = VGroup()
            angles = [0, 72, 144, 216, 288] 
            radius = 0.65
            for angle in angles:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * radius, np.sin(rad) * radius, 0])
                spokes.add(Line(start=ORIGIN, end=pos, color=ICON_BASE_COLOR, stroke_width=2))
                nodes.add(Circle(radius=0.08, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(pos))
            network = VGroup(spokes, hub, nodes)
            box = Square(side_length=1.8, color=ICON_BASE_COLOR, stroke_width=2)
            icon_group = VGroup(box, network)
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(icon_group, UP, buff=0.1)
            return VGroup(icon_group, label)

        def get_db_icon():
            front_sq = Square(side_length=0.9, color=ICON_BASE_COLOR)
            back_sq = Square(side_length=0.9, color=ICON_BASE_COLOR).shift(UP*0.25 + RIGHT*0.25)
            connectors = VGroup(
                Line(front_sq.get_corner(UL), back_sq.get_corner(UL), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(UR), back_sq.get_corner(UR), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(DL), back_sq.get_corner(DL), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(DR), back_sq.get_corner(DR), color=ICON_BASE_COLOR),
            )
            dots = VGroup(
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + LEFT*0.15),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(back_sq.get_center() + RIGHT*0.15 + UP*0.1),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + DOWN*0.15 + RIGHT*0.1),
            )
            icon_group = VGroup(back_sq, front_sq, connectors, dots)
            label = Text("Vector Database", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.1)
            return VGroup(icon_group, label)

        def get_llm_icon():
            circle = Circle(radius=0.6, color=ICON_BASE_COLOR, stroke_width=3)
            text = Text("LLM", font_size=24, color=TEXT_COLOR, weight=BOLD).move_to(circle)
            return VGroup(circle, text)

        def get_fine_tuning_icon():
            circle = Circle(radius=0.35, color=ICON_BASE_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            text = Text("Fine\nTuning", font_size=10, color=TEXT_COLOR, line_spacing=1).move_to(circle)
            return VGroup(circle, text)

        def get_content_icons():
            def make_doc(color):
                doc = Rectangle(height=0.5, width=0.35, color=color, stroke_width=1.5)
                corner = Polygon(
                    doc.get_corner(UR), 
                    doc.get_corner(UR)+LEFT*0.12, 
                    doc.get_corner(UR)+DOWN*0.12+LEFT*0.12, 
                    doc.get_corner(UR)+DOWN*0.12, 
                    color=color, stroke_width=1.5, fill_color=BACKGROUND_COLOR, fill_opacity=1
                )
                return VGroup(doc, corner)

            orig_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(6)]).arrange_in_grid(rows=2, buff=0.08)
            new_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(4)]).arrange_in_grid(rows=2, buff=0.08)
            all_docs = VGroup(orig_docs, new_docs).arrange(RIGHT, buff=0.3)
            orig_label = Text("Original Content", font_size=12, color=PRIMARY_COLOR).next_to(orig_docs, DOWN, buff=0.1)
            new_label = Text("New Content", font_size=12, color=PRIMARY_COLOR).next_to(new_docs, DOWN, buff=0.1)
            return VGroup(all_docs, orig_label, new_label)

        def get_number_circle(number):
            circle = Circle(radius=0.15, color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=1)
            num = Text(str(number), color=WHITE, font_size=16, weight=BOLD).move_to(circle)
            return VGroup(circle, num)

        def create_straight_arrow(start_point, end_point, color=ICON_BASE_COLOR):
            line = Line(start=start_point, end=end_point, color=color, stroke_width=3)
            line.add_tip(tip_length=0.2, tip_width=0.2)
            return line

        # --- 2. Layout Positioning ---
        
        title = Text("RAG Architecture Model", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)

        framework = get_framework_icon().shift(UP*0.5) 
        client = get_client_icon().next_to(framework, LEFT, buff=2.0).shift(DOWN*0.2)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.0).shift(DOWN*0.2)
        db = get_db_icon().next_to(framework, DOWN, buff=1.5)
        content = get_content_icons().next_to(db, RIGHT, buff=0.8).align_to(db, DOWN)
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        ft_connector = DashedLine(
            start=fine_tuning.get_bottom(), 
            end=llm.get_top(), 
            color=ICON_BASE_COLOR, 
            stroke_width=2,
            dash_length=0.1
        )

        # Arrows - using matched Y/X coordinates for perfectly straight arrows
        # Horizontal arrows between Client and Framework
        y_level_1 = client[0].get_center()[1]
        arrow_c_f = create_straight_arrow(
            [client[0].get_right()[0] + 0.1, y_level_1, 0], 
            [framework[0].get_left()[0] - 0.1, y_level_1, 0]
        )
        y_level_2 = y_level_1 + 0.4
        arrow_f_c = create_straight_arrow(
            [framework[0].get_left()[0] - 0.1, y_level_2, 0], 
            [client[0].get_right()[0] + 0.1, y_level_2, 0]
        )
        
        # Horizontal arrows between Framework and LLM
        y_level_3 = framework[0].get_center()[1]
        arrow_f_llm = create_straight_arrow(
            [framework[0].get_right()[0] + 0.1, y_level_3, 0], 
            [llm[0].get_left()[0] - 0.1, y_level_3, 0]
        )
        y_level_4 = y_level_3 + 0.4
        arrow_llm_f = create_straight_arrow(
            [llm[0].get_left()[0] - 0.1, y_level_4, 0], 
            [framework[0].get_right()[0] + 0.1, y_level_4, 0]
        )
        
        # Vertical arrows between Framework and Database
        x_level_1 = framework[0].get_center()[0] - 0.4
        arrow_f_db = create_straight_arrow(
            [x_level_1, framework[0].get_bottom()[1] - 0.1, 0], 
            [x_level_1, db[0].get_top()[1] + 0.1, 0]
        )
        x_level_2 = framework[0].get_center()[0] + 0.4
        arrow_db_f = create_straight_arrow(
            [x_level_2, db[0].get_top()[1] + 0.1, 0], 
            [x_level_2, framework[0].get_bottom()[1] - 0.1, 0]
        )
        
        # Horizontal arrow from Content to Database
        y_level_5 = db[0].get_center()[1]
        arrow_content_db = create_straight_arrow(
            [content[0].get_left()[0] - 0.1, y_level_5, 0], 
            [db[0].get_right()[0] + 0.1, y_level_5, 0]
        )

        # Labels
        label_q = Text("Question", font_size=16, color=TEXT_COLOR).next_to(arrow_c_f, DOWN, buff=0.1)
        num_1 = get_number_circle(1).next_to(label_q, LEFT, buff=0.1)
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR).next_to(arrow_f_c, UP, buff=0.1)
        label_sem = Text("Semantic\nSearch", font_size=14, color=TEXT_COLOR, line_spacing=1).next_to(arrow_f_db, LEFT, buff=0.1)
        num_2 = get_number_circle(2).next_to(label_sem, DOWN, buff=0.1)
        label_ctx = Text("Contextual\nData", font_size=14, color=TEXT_COLOR, line_spacing=1).next_to(arrow_db_f, RIGHT, buff=0.1)
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR).next_to(arrow_f_llm, DOWN, buff=0.1)
        num_3 = get_number_circle(3).next_to(label_prompt, DOWN, buff=0.1)
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).next_to(arrow_llm_f, UP, buff=0.1)
        num_4 = get_number_circle(4).next_to(label_post, UP, buff=0.1)

        # Center Scene
        whole_scene = VGroup(
            client, framework, llm, db, content,
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f, arrow_f_db, arrow_db_f, arrow_content_db,
            label_q, num_1, label_resp, label_sem, num_2, label_ctx, label_prompt, num_3, label_post, num_4,
            fine_tuning, ft_connector
        )
        whole_scene.move_to(ORIGIN)

        # --- 3. Animation Sequence ---
        
        self.play(Write(title))
        self.play(
            LaggedStart(
                FadeIn(client), FadeIn(framework), FadeIn(db), FadeIn(llm), FadeIn(content), 
                FadeIn(fine_tuning), Create(ft_connector),
                lag_ratio=0.1
            ), run_time=1.5
        )
        self.wait(0.5)

        # Phase 0: Ingestion
        self.play(Create(arrow_content_db)) 
        self.wait(0.5)

        # Phase 1: Question
        arrow_c_f.set_color(PRIMARY_COLOR)
        self.play(Create(arrow_c_f), Write(label_q), FadeIn(num_1))
        self.wait(0.5)

        # Phase 2: Retrieval
        arrow_f_db.set_color(PRIMARY_COLOR)
        arrow_db_f.set_color(PRIMARY_COLOR)
        
        self.play(Create(arrow_f_db), Write(label_sem), FadeIn(num_2))
        
        self.play(Create(arrow_db_f), Write(label_ctx))
        self.wait(0.5)

        # Phase 3: Prompt
        arrow_f_llm.set_color(PRIMARY_COLOR)
        self.play(Create(arrow_f_llm), Write(label_prompt), FadeIn(num_3))
        self.wait(0.5)

        # Phase 4: Response
        arrow_llm_f.set_color(PRIMARY_COLOR)
        arrow_f_c.set_color(PRIMARY_COLOR)
        
        self.play(Create(arrow_llm_f), Write(label_post), FadeIn(num_4))
        
        self.play(Create(arrow_f_c), Write(label_resp))

        self.wait(3)

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             
ICON_BASE_COLOR = "#ec5599"    # Lighter Grey
BACKGROUND_COLOR = WHITE       
LIGHT_PINK = "#fbcfe8"         

class RAGZoomScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers (Thinner stroke widths) ---
        def get_client_icon():
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            body = AnnularSector(inner_radius=0, outer_radius=0.5, start_angle=PI, angle=-PI, color=LIGHT_PINK, fill_opacity=1)
            body.stretch(1.2, dim=1) 
            body.shift(DOWN * 0.15)
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.0)
            spokes = VGroup()
            nodes = VGroup()
            angles = [0, 72, 144, 216, 288] 
            radius = 0.65
            for angle in angles:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * radius, np.sin(rad) * radius, 0])
                spokes.add(Line(start=ORIGIN, end=pos, color=ICON_BASE_COLOR, stroke_width=1.5))
                nodes.add(Circle(radius=0.08, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=1.5).move_to(pos))
            network = VGroup(spokes, hub, nodes)
            box = Square(side_length=1.8, color=ICON_BASE_COLOR, stroke_width=1.5)
            icon_group = VGroup(box, network)
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(icon_group, UP, buff=0.1)
            return VGroup(icon_group, label)

        def get_db_icon():
            front_sq = Square(side_length=0.9, color=ICON_BASE_COLOR, stroke_width=1.5)
            back_sq = Square(side_length=0.9, color=ICON_BASE_COLOR, stroke_width=1.5).shift(UP*0.25 + RIGHT*0.25)
            connectors = VGroup(
                Line(front_sq.get_corner(UL), back_sq.get_corner(UL), color=ICON_BASE_COLOR, stroke_width=1.5),
                Line(front_sq.get_corner(UR), back_sq.get_corner(UR), color=ICON_BASE_COLOR, stroke_width=1.5),
                Line(front_sq.get_corner(DL), back_sq.get_corner(DL), color=ICON_BASE_COLOR, stroke_width=1.5),
                Line(front_sq.get_corner(DR), back_sq.get_corner(DR), color=ICON_BASE_COLOR, stroke_width=1.5),
            )
            dots = VGroup(
                Dot(color=ICON_BASE_COLOR, radius=0.04).move_to(front_sq.get_center() + LEFT*0.15),
                Dot(color=ICON_BASE_COLOR, radius=0.04).move_to(back_sq.get_center() + RIGHT*0.15 + UP*0.1),
                Dot(color=ICON_BASE_COLOR, radius=0.04).move_to(front_sq.get_center() + DOWN*0.15 + RIGHT*0.1),
            )
            icon_group = VGroup(back_sq, front_sq, connectors, dots)
            label = Text("Vector Database", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.1)
            return VGroup(icon_group, label)

        def get_llm_icon():
            circle = Circle(radius=0.6, color=ICON_BASE_COLOR, stroke_width=2.5)
            text = Text("LLM", font_size=24, color=TEXT_COLOR, weight=BOLD).move_to(circle)
            return VGroup(circle, text)

        def get_fine_tuning_icon():
            circle = Circle(radius=0.35, color=ICON_BASE_COLOR, stroke_width=1.5, fill_color=WHITE, fill_opacity=1)
            text = Text("Fine\nTuning", font_size=10, color=TEXT_COLOR, line_spacing=1).move_to(circle)
            return VGroup(circle, text)

        def get_content_icons():
            def make_doc(color):
                doc = Rectangle(height=0.5, width=0.35, color=color, stroke_width=1.5)
                corner = Polygon(doc.get_corner(UR), doc.get_corner(UR)+LEFT*0.12, doc.get_corner(UR)+DOWN*0.12+LEFT*0.12, doc.get_corner(UR)+DOWN*0.12, color=color, stroke_width=1.5, fill_color=BACKGROUND_COLOR, fill_opacity=1)
                return VGroup(doc, corner)
            orig_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(6)]).arrange_in_grid(rows=2, buff=0.08)
            new_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(4)]).arrange_in_grid(rows=2, buff=0.08)
            all_docs = VGroup(orig_docs, new_docs).arrange(RIGHT, buff=0.3)
            orig_label = Text("Original Content", font_size=12, color=PRIMARY_COLOR).next_to(orig_docs, DOWN, buff=0.1)
            new_label = Text("New Content", font_size=12, color=PRIMARY_COLOR).next_to(new_docs, DOWN, buff=0.1)
            return VGroup(all_docs, orig_label, new_label)

        def create_straight_arrow(start, end, color=ICON_BASE_COLOR):
            line = Line(start=start, end=end, color=color, stroke_width=2.0)
            line.add_tip(tip_length=0.2, tip_width=0.2)
            return line

        # --- 2. Build Scene Layout ---
        title = Text("RAG Architecture Model", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)

        framework = get_framework_icon().shift(UP*0.5) 
        client = get_client_icon().next_to(framework, LEFT, buff=2.0).shift(DOWN*0.2)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.0).shift(DOWN*0.2)
        db = get_db_icon().next_to(framework, DOWN, buff=1.5)
        content = get_content_icons().next_to(db, RIGHT, buff=0.8).align_to(db, DOWN)
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        ft_connector = DashedLine(start=fine_tuning.get_bottom(), end=llm.get_top(), color=ICON_BASE_COLOR, stroke_width=1.5, dash_length=0.1)

        # Arrows - using matched Y/X coordinates for perfectly straight arrows
        # Horizontal arrows between Client and Framework
        y_level_1 = client[0].get_center()[1]
        arrow_c_f = create_straight_arrow(
            [client[0].get_right()[0] + 0.1, y_level_1, 0], 
            [framework[0].get_left()[0] - 0.1, y_level_1, 0]
        )
        y_level_2 = y_level_1 + 0.4
        arrow_f_c = create_straight_arrow(
            [framework[0].get_left()[0] - 0.1, y_level_2, 0], 
            [client[0].get_right()[0] + 0.1, y_level_2, 0]
        )
        
        # Horizontal arrows between Framework and LLM
        y_level_3 = framework[0].get_center()[1]
        arrow_f_llm = create_straight_arrow(
            [framework[0].get_right()[0] + 0.1, y_level_3, 0], 
            [llm[0].get_left()[0] - 0.1, y_level_3, 0]
        )
        y_level_4 = y_level_3 + 0.4
        arrow_llm_f = create_straight_arrow(
            [llm[0].get_left()[0] - 0.1, y_level_4, 0], 
            [framework[0].get_right()[0] + 0.1, y_level_4, 0]
        )
        
        # Vertical arrows between Framework and Database
        x_level_1 = framework[0].get_center()[0] - 0.4
        arrow_f_db = create_straight_arrow(
            [x_level_1, framework[0].get_bottom()[1] - 0.1, 0], 
            [x_level_1, db[0].get_top()[1] + 0.1, 0]
        )
        x_level_2 = framework[0].get_center()[0] + 0.4
        arrow_db_f = create_straight_arrow(
            [x_level_2, db[0].get_top()[1] + 0.1, 0], 
            [x_level_2, framework[0].get_bottom()[1] - 0.1, 0]
        )
        
        # Horizontal arrow from Content to Database
        y_level_5 = db[0].get_center()[1]
        arrow_content_db = create_straight_arrow(
            [content[0].get_left()[0] - 0.1, y_level_5, 0], 
            [db[0].get_right()[0] + 0.1, y_level_5, 0]
        )

        # Labels
        label_q = Text("Question", font_size=16, color=TEXT_COLOR).next_to(arrow_c_f, DOWN, buff=0.1)
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR).next_to(arrow_f_c, UP, buff=0.1)
        label_sem = Text("Semantic\nSearch", font_size=14, color=TEXT_COLOR, line_spacing=1).next_to(arrow_f_db, LEFT, buff=0.1)
        label_ctx = Text("Contextual\nData", font_size=14, color=TEXT_COLOR, line_spacing=1).next_to(arrow_db_f, RIGHT, buff=0.1)
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR).next_to(arrow_f_llm, DOWN, buff=0.1)
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).next_to(arrow_llm_f, UP, buff=0.1)

        # 3. Main Container
        all_elements = VGroup(
            title, client, framework, llm, db, content, fine_tuning, ft_connector,
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f, arrow_f_db, arrow_db_f, arrow_content_db,
            label_q, label_resp, label_sem, label_ctx, label_prompt, label_post
        )

        # --- 4. Animation Sequence ---
        self.add(all_elements)
        self.camera.frame.save_state() 

        self.wait(2)

        # --- ZOOM 1: LLM ---
        try:
            llm_img = ImageMobject(r"D:\manim\images\llm.jpg").set_height(1.875)  # 0.75x of 2.5
        except:
            rect = Rectangle(color=RED, fill_opacity=0.5, height=1.875, width=3)
            t = Text("LLM.jpg", color=WHITE, font_size=18).move_to(rect)
            llm_img = Group(rect, t)
        
        watch_text_1 = Text("Watch this video", font_size=28, color=PRIMARY_COLOR, weight=BOLD)
        
        # Position elements: LLM stays in place, watch text and image go to the RIGHT side
        watch_text_1.next_to(llm, RIGHT, buff=1.5).shift(DOWN * 0.5)
        llm_img.next_to(watch_text_1, DOWN, buff=0.5)
        
        focus_group_1 = Group(llm, watch_text_1, llm_img)

        self.play(
            all_elements.animate.set_opacity(0.15),
            llm.animate.set_opacity(1),
            self.camera.frame.animate.move_to(focus_group_1.get_center()).set(height=focus_group_1.height * 1.6),
            run_time=2
        )
        self.play(FadeIn(watch_text_1), FadeIn(llm_img))
        self.wait(3)
        
        self.play(FadeOut(watch_text_1), FadeOut(llm_img), run_time=0.5)
        self.play(
            Restore(self.camera.frame), 
            all_elements.animate.set_opacity(1), 
            run_time=1.5
        )

        # --- ZOOM 2: Semantic Search ---
        try:
            sem_img = ImageMobject(r"D:\manim\images\semantic.jpg").set_height(1.875)  # 0.75x of 2.5
        except:
            rect = Rectangle(color=GREEN, fill_opacity=0.5, height=1.875, width=3)
            t = Text("semantic.jpg", color=WHITE, font_size=18).move_to(rect)
            sem_img = Group(rect, t)

        watch_text_2 = Text("Watch this video", font_size=28, color=PRIMARY_COLOR, weight=BOLD)
        
        # Position elements: Semantic label stays in place, watch text and image go to the LEFT side
        watch_text_2.next_to(label_sem, LEFT, buff=1.5).shift(DOWN * 0.5)
        sem_img.next_to(watch_text_2, DOWN, buff=0.5)
        
        focus_group_2 = Group(label_sem, watch_text_2, sem_img)

        self.play(
            all_elements.animate.set_opacity(0.15),
            label_sem.animate.set_opacity(1),
            self.camera.frame.animate.move_to(focus_group_2.get_center()).set(height=focus_group_2.height * 1.6),
            run_time=2
        )
        self.play(FadeIn(watch_text_2), FadeIn(sem_img))
        self.wait(3)

        self.play(FadeOut(watch_text_2), FadeOut(sem_img), run_time=0.5)
        self.play(
            Restore(self.camera.frame), 
            all_elements.animate.set_opacity(1), 
            run_time=1.5
        )

        # --- ZOOM 3: Fine Tuning ---
        try:
            ft_img = ImageMobject(r"D:\manim\images\finetuning.jpg").set_height(1.875)  # 0.75x of 2.5
        except:
            rect = Rectangle(color=BLUE, fill_opacity=0.5, height=1.875, width=3)
            t = Text("finetuning.jpg", color=WHITE, font_size=18).move_to(rect)
            ft_img = Group(rect, t)

        watch_text_3 = Text("Watch this video", font_size=28, color=PRIMARY_COLOR, weight=BOLD)
        
        # Position elements: Fine Tuning stays, watch text and image slightly to the RIGHT and DOWN for center positioning
        watch_text_3.next_to(fine_tuning, RIGHT, buff=1.2).shift(DOWN * 0.3)
        ft_img.next_to(watch_text_3, DOWN, buff=0.5)
        
        focus_group_3 = Group(fine_tuning, watch_text_3, ft_img)

        self.play(
            all_elements.animate.set_opacity(0.15),
            fine_tuning.animate.set_opacity(1),
            self.camera.frame.animate.move_to(focus_group_3.get_center()).set(height=focus_group_3.height * 1.6),
            run_time=2
        )
        self.play(FadeIn(watch_text_3), FadeIn(ft_img))
        self.wait(3)

        self.play(FadeOut(watch_text_3), FadeOut(ft_img), run_time=0.5)
        self.play(
            Restore(self.camera.frame), 
            all_elements.animate.set_opacity(1), 
            run_time=1.5
        )

        self.wait(2)


from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Highlights, Numbers)
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # Black text for white background
ICON_BASE_COLOR = "#ec5599"    # Dark Grey (Change this to update all icons!)
BACKGROUND_COLOR = WHITE       # White background
LIGHT_PINK = "#fbcfe8"         # Solid Light Pink for Client

class RAGArchitectureScene2(Scene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers ---

        def get_client_icon():
            # Proportional User Icon with larger head
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            
            body = AnnularSector(
                inner_radius=0, 
                outer_radius=0.5, 
                start_angle=PI, 
                angle=-PI, 
                color=LIGHT_PINK, 
                fill_opacity=1
            )
            body.stretch(1.2, dim=1) 
            body.shift(DOWN * 0.15)
            
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.5)
            spokes = VGroup()
            nodes = VGroup()
            angles = [0, 72, 144, 216, 288] 
            radius = 0.65
            for angle in angles:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * radius, np.sin(rad) * radius, 0])
                spokes.add(Line(start=ORIGIN, end=pos, color=ICON_BASE_COLOR, stroke_width=2))
                nodes.add(Circle(radius=0.08, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(pos))
            network = VGroup(spokes, hub, nodes)
            box = Square(side_length=1.8, color=ICON_BASE_COLOR, stroke_width=2)
            icon_group = VGroup(box, network)
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(icon_group, UP, buff=0.1)
            return VGroup(icon_group, label)

        def get_db_icon():
            front_sq = Square(side_length=0.9, color=ICON_BASE_COLOR)
            back_sq = Square(side_length=0.9, color=ICON_BASE_COLOR).shift(UP*0.25 + RIGHT*0.25)
            connectors = VGroup(
                Line(front_sq.get_corner(UL), back_sq.get_corner(UL), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(UR), back_sq.get_corner(UR), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(DL), back_sq.get_corner(DL), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(DR), back_sq.get_corner(DR), color=ICON_BASE_COLOR),
            )
            dots = VGroup(
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + LEFT*0.15),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(back_sq.get_center() + RIGHT*0.15 + UP*0.1),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + DOWN*0.15 + RIGHT*0.1),
            )
            icon_group = VGroup(back_sq, front_sq, connectors, dots)
            label = Text("Vector Database", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.1)
            return VGroup(icon_group, label)

        def get_llm_icon():
            circle = Circle(radius=0.6, color=ICON_BASE_COLOR, stroke_width=3)
            text = Text("LLM", font_size=24, color=TEXT_COLOR, weight=BOLD).move_to(circle)
            return VGroup(circle, text)

        def get_fine_tuning_icon():
            circle = Circle(radius=0.35, color=ICON_BASE_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            text = Text("Fine\nTuning", font_size=10, color=TEXT_COLOR, line_spacing=1).move_to(circle)
            return VGroup(circle, text)

        def get_content_icons():
            def make_doc(color):
                doc = Rectangle(height=0.5, width=0.35, color=color, stroke_width=1.5)
                corner = Polygon(
                    doc.get_corner(UR), 
                    doc.get_corner(UR)+LEFT*0.12, 
                    doc.get_corner(UR)+DOWN*0.12+LEFT*0.12, 
                    doc.get_corner(UR)+DOWN*0.12, 
                    color=color, stroke_width=1.5, fill_color=BACKGROUND_COLOR, fill_opacity=1
                )
                return VGroup(doc, corner)

            orig_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(6)]).arrange_in_grid(rows=2, buff=0.08)
            new_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(4)]).arrange_in_grid(rows=2, buff=0.08)
            all_docs = VGroup(orig_docs, new_docs).arrange(RIGHT, buff=0.3)
            orig_label = Text("Original Content", font_size=12, color=PRIMARY_COLOR).next_to(orig_docs, DOWN, buff=0.1)
            new_label = Text("New Content", font_size=12, color=PRIMARY_COLOR).next_to(new_docs, DOWN, buff=0.1)
            return VGroup(all_docs, orig_label, new_label)

        def get_number_circle(number):
            circle = Circle(radius=0.15, color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=1)
            num = Text(str(number), color=WHITE, font_size=16, weight=BOLD).move_to(circle)
            return VGroup(circle, num)

        def create_straight_arrow(start_point, end_point, color=ICON_BASE_COLOR):
            line = Line(start=start_point, end=end_point, color=color, stroke_width=3)
            line.add_tip(tip_length=0.2, tip_width=0.2)
            return line

        # --- 2. Layout Positioning ---
        
        # Title is pinned to edge, do not include in centered group later
        title = Text("RAG Architecture Model", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)

        framework = get_framework_icon().shift(UP*0.5) 
        client = get_client_icon().next_to(framework, LEFT, buff=2.0).shift(DOWN*0.2)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.0).shift(DOWN*0.2)
        db = get_db_icon().next_to(framework, DOWN, buff=1.5)
        content = get_content_icons().next_to(db, RIGHT, buff=0.8).align_to(db, DOWN)
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        ft_connector = DashedLine(
            start=fine_tuning.get_bottom(), 
            end=llm.get_top(), 
            color=ICON_BASE_COLOR, 
            stroke_width=2,
            dash_length=0.1
        )

        # Arrows - using matched Y/X coordinates for perfectly straight arrows
        # Horizontal arrows between Client and Framework
        y_level_1 = client[0].get_center()[1]
        arrow_c_f = create_straight_arrow(
            [client[0].get_right()[0] + 0.1, y_level_1, 0], 
            [framework[0].get_left()[0] - 0.1, y_level_1, 0]
        )
        y_level_2 = y_level_1 + 0.4
        arrow_f_c = create_straight_arrow(
            [framework[0].get_left()[0] - 0.1, y_level_2, 0], 
            [client[0].get_right()[0] + 0.1, y_level_2, 0]
        )
        
        # Horizontal arrows between Framework and LLM
        y_level_3 = framework[0].get_center()[1]
        arrow_f_llm = create_straight_arrow(
            [framework[0].get_right()[0] + 0.1, y_level_3, 0], 
            [llm[0].get_left()[0] - 0.1, y_level_3, 0]
        )
        y_level_4 = y_level_3 + 0.4
        arrow_llm_f = create_straight_arrow(
            [llm[0].get_left()[0] - 0.1, y_level_4, 0], 
            [framework[0].get_right()[0] + 0.1, y_level_4, 0]
        )
        
        # Vertical arrows between Framework and Database
        x_level_1 = framework[0].get_center()[0] - 0.4
        arrow_f_db = create_straight_arrow(
            [x_level_1, framework[0].get_bottom()[1] - 0.1, 0], 
            [x_level_1, db[0].get_top()[1] + 0.1, 0]
        )
        x_level_2 = framework[0].get_center()[0] + 0.4
        arrow_db_f = create_straight_arrow(
            [x_level_2, db[0].get_top()[1] + 0.1, 0], 
            [x_level_2, framework[0].get_bottom()[1] - 0.1, 0]
        )
        
        # Horizontal arrow from Content to Database
        y_level_5 = db[0].get_center()[1]
        arrow_content_db = create_straight_arrow(
            [content[0].get_left()[0] - 0.1, y_level_5, 0], 
            [db[0].get_right()[0] + 0.1, y_level_5, 0]
        )

        # Labels
        label_q = Text("Question", font_size=16, color=TEXT_COLOR).next_to(arrow_c_f, DOWN, buff=0.1)
        num_1 = get_number_circle(1).next_to(label_q, LEFT, buff=0.1)
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR).next_to(arrow_f_c, UP, buff=0.1)
        label_sem = Text("Semantic\nSearch", font_size=14, color=TEXT_COLOR, line_spacing=1).next_to(arrow_f_db, LEFT, buff=0.1)
        num_2 = get_number_circle(2).next_to(label_sem, DOWN, buff=0.1)
        label_ctx = Text("Contextual\nData", font_size=14, color=TEXT_COLOR, line_spacing=1).next_to(arrow_db_f, RIGHT, buff=0.1)
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR).next_to(arrow_f_llm, DOWN, buff=0.1)
        num_3 = get_number_circle(3).next_to(label_prompt, DOWN, buff=0.1)
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).next_to(arrow_llm_f, UP, buff=0.1)
        num_4 = get_number_circle(4).next_to(label_post, UP, buff=0.1)

        # Set colors for items that start highlighted
        arrow_c_f.set_color(PRIMARY_COLOR)
        arrow_f_db.set_color(PRIMARY_COLOR)
        arrow_db_f.set_color(PRIMARY_COLOR)
        arrow_f_llm.set_color(PRIMARY_COLOR)
        arrow_llm_f.set_color(PRIMARY_COLOR)
        arrow_f_c.set_color(PRIMARY_COLOR)

        # Center Scene (Group only the diagram parts, excluding title)
        diagram_group = VGroup(
            client, framework, llm, db, content,
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f, arrow_f_db, arrow_db_f, arrow_content_db,
            label_q, num_1, label_resp, label_sem, num_2, label_ctx, label_prompt, num_3, label_post, num_4,
            fine_tuning, ft_connector
        )
        diagram_group.move_to(ORIGIN)

        # --- 3. Animation Sequence ---
        
        # Show everything at once (Title pinned, diagram centered)
        self.add(title, diagram_group)
        self.wait(2)

        # --- New Fade Out Animation ---
        # Group elements to fade: LLM hub, Prompt loop (3), Post-processing loop (4), Response loop
        elements_to_fade = VGroup(
            llm, fine_tuning, ft_connector,       # The LLM block
            label_prompt, num_3, arrow_f_llm,     # Prompt loop
            label_post, num_4, arrow_llm_f,       # Post-processing loop
            label_resp, arrow_f_c                 # Response loop
        )

        # Fade them out slowly over 3 seconds
        self.play(FadeOut(elements_to_fade), run_time=3)
        self.wait(5)

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Highlights, Numbers)
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # Black text for white background
ICON_BASE_COLOR = "#ec5599"    # Medium Pink/Grey for icons
BACKGROUND_COLOR = WHITE       # White background
LIGHT_PINK = "#fbcfe8"         # Solid Light Pink for Client
GREEN_COLOR = "#16a34a"        # Green for similarity scores

class RAGScenarioScene(Scene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers ---

        def get_client_icon():
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            body = AnnularSector(
                inner_radius=0, outer_radius=0.5, start_angle=PI, angle=-PI, 
                color=LIGHT_PINK, fill_opacity=1
            )
            body.stretch(1.2, dim=1)
            body.shift(DOWN * 0.15)
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.5)
            spokes = VGroup()
            nodes = VGroup()
            angles = [0, 72, 144, 216, 288] 
            radius = 0.65
            for angle in angles:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * radius, np.sin(rad) * radius, 0])
                spokes.add(Line(start=ORIGIN, end=pos, color=ICON_BASE_COLOR, stroke_width=2))
                nodes.add(Circle(radius=0.08, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(pos))
            network = VGroup(spokes, hub, nodes)
            box = Square(side_length=1.8, color=ICON_BASE_COLOR, stroke_width=2)
            icon_group = VGroup(box, network)
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(icon_group, UP, buff=0.1)
            return VGroup(icon_group, label)

        def get_db_icon():
            front_sq = Square(side_length=0.9, color=ICON_BASE_COLOR)
            back_sq = Square(side_length=0.9, color=ICON_BASE_COLOR).shift(UP*0.25 + RIGHT*0.25)
            connectors = VGroup(
                Line(front_sq.get_corner(UL), back_sq.get_corner(UL), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(UR), back_sq.get_corner(UR), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(DL), back_sq.get_corner(DL), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(DR), back_sq.get_corner(DR), color=ICON_BASE_COLOR),
            )
            dots = VGroup(
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + LEFT*0.15),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(back_sq.get_center() + RIGHT*0.15 + UP*0.1),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + DOWN*0.15 + RIGHT*0.1),
            )
            icon_group = VGroup(back_sq, front_sq, connectors, dots)
            label = Text("Vector Database", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.1)
            return VGroup(icon_group, label)

        def get_content_icons():
            def make_doc(color):
                doc = Rectangle(height=0.5, width=0.35, color=color, stroke_width=1.5)
                corner = Polygon(
                    doc.get_corner(UR), doc.get_corner(UR)+LEFT*0.12, 
                    doc.get_corner(UR)+DOWN*0.12+LEFT*0.12, doc.get_corner(UR)+DOWN*0.12, 
                    color=color, stroke_width=1.5, fill_color=BACKGROUND_COLOR, fill_opacity=1
                )
                return VGroup(doc, corner)

            orig_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(6)]).arrange_in_grid(rows=2, buff=0.08)
            new_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(4)]).arrange_in_grid(rows=2, buff=0.08)
            all_docs = VGroup(orig_docs, new_docs).arrange(RIGHT, buff=0.3)
            orig_label = Text("Original Content", font_size=12, color=PRIMARY_COLOR).next_to(orig_docs, DOWN, buff=0.1)
            new_label = Text("New Content", font_size=12, color=PRIMARY_COLOR).next_to(new_docs, DOWN, buff=0.1)
            return VGroup(all_docs, orig_label, new_label)

        def create_straight_arrow(start_point, end_point, color=ICON_BASE_COLOR):
            line = Line(start=start_point, end=end_point, color=color, stroke_width=3)
            line.add_tip(tip_length=0.2, tip_width=0.2)
            return line

        # --- 2. Initial State Setup ---
        
        title = Text("RAG Architecture Model", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)
        
        framework = get_framework_icon().shift(UP*0.5) 
        client = get_client_icon().next_to(framework, LEFT, buff=2.0).shift(DOWN*0.2)
        db = get_db_icon().next_to(framework, DOWN, buff=1.5)
        content = get_content_icons().next_to(db, RIGHT, buff=0.8).align_to(db, DOWN)
        
        orig_docs_group = content[0][0]
        new_docs_group = content[0][1]
        orig_label = content[1]
        new_label = content[2]

        # Fixed straight arrows
        y_level_1 = client[0].get_center()[1]
        arrow_c_f = create_straight_arrow(
            [client[0].get_right()[0] + 0.1, y_level_1, 0], 
            [framework[0].get_left()[0] - 0.1, y_level_1, 0],
            color=PRIMARY_COLOR
        )
        
        x_level_1 = framework[0].get_center()[0] - 0.4
        arrow_f_db = create_straight_arrow(
            [x_level_1, framework[0].get_bottom()[1] - 0.1, 0], 
            [x_level_1, db[0].get_top()[1] + 0.1, 0],
            color=PRIMARY_COLOR
        )
        
        x_level_2 = framework[0].get_center()[0] + 0.4
        arrow_db_f = create_straight_arrow(
            [x_level_2, db[0].get_top()[1] + 0.1, 0], 
            [x_level_2, framework[0].get_bottom()[1] - 0.1, 0],
            color=PRIMARY_COLOR
        )
        
        y_level_2 = db[0].get_center()[1]
        arrow_content_db = create_straight_arrow(
            [content[0].get_left()[0] - 0.1, y_level_2, 0], 
            [db[0].get_right()[0] + 0.1, y_level_2, 0],
            color=ICON_BASE_COLOR
        )

        label_q = Text("Question", font_size=16, color=TEXT_COLOR).next_to(arrow_c_f, DOWN, buff=0.1)
        label_sem = Text("Semantic\nSearch", font_size=14, color=TEXT_COLOR, line_spacing=1).next_to(arrow_f_db, LEFT, buff=0.1)
        label_ctx = Text("Contextual\nData", font_size=14, color=TEXT_COLOR, line_spacing=1).next_to(arrow_db_f, RIGHT, buff=0.1)

        diagram_group = VGroup(
            client, framework, db, content,
            arrow_c_f, arrow_f_db, arrow_db_f, arrow_content_db,
            label_q, label_sem, label_ctx
        )
        diagram_group.move_to(ORIGIN)

        self.add(title, diagram_group)
        self.wait(1)

        # --- 3. Transition Sequence ---

        # 1. Fade out unnecessary elements
        items_to_fade = VGroup(
            title, framework, db, 
            orig_docs_group, orig_label, new_label, 
            arrow_c_f, arrow_f_db, arrow_db_f, arrow_content_db,
            label_q, label_sem, label_ctx
        )
        
        self.play(FadeOut(items_to_fade), run_time=1.5)
        
        # 2. Create Question Box (Invisible for now)
        q_text = "Question: I work remotely. Can I expense a\n$1,200 monitor that I use for my work?"
        q_box = Rectangle(height=1.5, width=6.0, color=ICON_BASE_COLOR, fill_color=LIGHT_PINK, fill_opacity=0.2)
        q_content = Text(q_text, font_size=20, color=TEXT_COLOR, line_spacing=1.2).move_to(q_box)
        q_group = VGroup(q_box, q_content)

        # 3. Calculate Final Positions for Centering
        # Create a temporary group to figure out the arrangement
        temp_top_group = VGroup(client.copy(), q_group.copy()).arrange(RIGHT, buff=0.5)
        # Move this temporary group to the desired top position
        temp_top_group.move_to(UP * 2.5)
        
        # Extract the target positions for the real objects
        target_client_pos = temp_top_group[0].get_center()
        target_q_group_pos = temp_top_group[1].get_center()
        
        # Place the invisible question group at its target position
        q_group.move_to(target_q_group_pos)

        # 4. Animate Client and Question to their centered positions
        self.play(
            client.animate.move_to(target_client_pos),
            FadeIn(q_group, shift=LEFT),
            run_time=2.0
        )
        
        # Define the final top group for reference
        top_group = VGroup(client, q_group)
        self.wait(0.5)

        # 5. Setup Cards Data with similarity scores
        card_data = [
            ("Company Expense Policy", "PDF", 0.75, 
             "Home office equipment\nup to $1,000 requires\nmanager approval."),
            ("HR Addendum", "Word Doc", 0.68,
             "Remote employees may\nexpense additional\nequipment once per year."),
            ("Email from Finance", "Text", 0.92,
             "Monitor reimbursements\nabove $800 are\ntemporarily paused."),
            ("Employee Profile", "Data", 0.61,
             "Role: Software Engineer\nRemote Status: Yes")
        ]

        # Prepare list to hold the Card Backgrounds and Card Texts separately
        card_bgs = VGroup()
        card_contents = VGroup() # Holds title, type, similarity, lines, body, correctness

        for i, (title_text, type_text, similarity, body_text) in enumerate(card_data):
            # Adjusted card height to fit content better
            card_bg = RoundedRectangle(corner_radius=0.15, height=4.2, width=3.2, color=PRIMARY_COLOR, 
                                       stroke_width=2.5, fill_color=WHITE, fill_opacity=1)
            
            # --- Header Content ---
            t_obj = Text(title_text, font_size=16, color=PRIMARY_COLOR, weight=BOLD).move_to(card_bg.get_top() + DOWN*0.4)
            if t_obj.width > 2.8:
                t_obj.scale_to_fit_width(2.8)
            
            type_obj = Text(f"({type_text})", font_size=14, color=ICON_BASE_COLOR, slant=ITALIC).next_to(t_obj, DOWN, buff=0.1)
            
            # Top Separator Line (Fixed Padding to stay within bounds)
            # 0.25 padding on each side ensures it doesn't touch the edges
            line1 = Line(
                card_bg.get_left() + RIGHT*0.25, 
                card_bg.get_right() + LEFT*0.25, 
                color=ICON_BASE_COLOR, stroke_width=1
            ).next_to(type_obj, DOWN, buff=0.15)
            
            # --- Body Content ---
            # INCREASED SIZE: Similarity Score
            sim_text = f"✓ Similarity Score: {similarity:.2f}"
            sim_obj = Text(sim_text, font_size=15, color=GREEN_COLOR, weight=BOLD).next_to(line1, DOWN, buff=0.15)
            sim_obj.align_to(card_bg.get_left() + RIGHT*0.25, LEFT)
            
            lines = body_text.split('\n')
            b_obj = VGroup(*[Text(l, font_size=14, color=TEXT_COLOR) for l in lines]).arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.08)
            b_obj.next_to(sim_obj, DOWN, buff=0.2)
            b_obj.align_to(card_bg.get_left() + RIGHT*0.25, LEFT)
            
            if b_obj.width > 2.7:
                b_obj.scale_to_fit_width(2.7)
            
            # --- Footer Content (Anchored to Bottom) ---
            
            # 1. Correctness Text (Anchored relative to bottom of card)
            correctness_obj = Text("Correctness?", font_size=13, color=PRIMARY_COLOR, weight=BOLD)
            correctness_obj.move_to(card_bg.get_bottom() + UP * 0.35) 
            
            # 2. Bottom Separator Line (Anchored just above Correctness)
            line2 = Line(
                card_bg.get_left() + RIGHT*0.25, 
                card_bg.get_right() + LEFT*0.25, 
                color=ICON_BASE_COLOR, stroke_width=1
            ).next_to(correctness_obj, UP, buff=0.15)
            
            card_bgs.add(card_bg)
            card_contents.add(VGroup(t_obj, type_obj, line1, sim_obj, b_obj, line2, correctness_obj))

        # Arrange backgrounds first to get positions
        card_bgs.arrange(RIGHT, buff=0.25)
        card_bgs.next_to(top_group, DOWN, buff=0.5)
        if card_bgs.width > 13.5:
             card_bgs.scale_to_fit_width(13.5)

        # Move contents to match their backgrounds' final positions
        for bg, content in zip(card_bgs, card_contents):
            t, ty, l1, sim, b, l2, corr = content
            
            # Re-position Header
            t.move_to(bg.get_top() + DOWN*0.4)
            ty.next_to(t, DOWN, buff=0.1)
            
            # Re-position Top Line (strictly bound by bg width)
            l1.put_start_and_end_on(bg.get_left() + RIGHT*0.25, bg.get_right() + LEFT*0.25)
            l1.next_to(ty, DOWN, buff=0.15)
            
            # Re-position Body
            sim.next_to(l1, DOWN, buff=0.15)
            sim.align_to(bg.get_left() + RIGHT*0.25, LEFT)
            b.next_to(sim, DOWN, buff=0.2)
            b.align_to(bg.get_left() + RIGHT*0.25, LEFT)
            
            # Re-position Footer (Anchored to Bottom)
            corr.move_to(bg.get_bottom() + UP * 0.35)
            l2.put_start_and_end_on(bg.get_left() + RIGHT*0.25, bg.get_right() + LEFT*0.25)
            l2.next_to(corr, UP, buff=0.15)

        # --- ANIMATION LOGIC: EXPAND AND POPULATE ---

        # 1. Move small docs to the center of where the large cards will be
        move_anims = []
        for i in range(4):
            move_anims.append(
                new_docs_group[i].animate.move_to(card_bgs[i].get_center())
            )
        self.play(*move_anims, run_time=1.5, rate_func=smooth)
        self.wait(0.1)

        # 2. Expand: Transform small docs into the Card Backgrounds
        expand_anims = []
        for i in range(4):
            expand_anims.append(
                ReplacementTransform(new_docs_group[i], card_bgs[i])
            )
        self.play(*expand_anims, run_time=1.0, rate_func=smooth)

        # 3. Populate: Fade in the text content
        self.play(FadeIn(card_contents, shift=UP*0.2), run_time=1.0)
        
        self.wait(4)

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Highlights, Numbers)
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # Black text for white background
ICON_BASE_COLOR = "#ec5599"    # Medium Pink/Grey for icons
BACKGROUND_COLOR = WHITE       # White background
LIGHT_PINK = "#fbcfe8"         # Solid Light Pink for Client

class RAGTransitionScene(Scene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers ---

        def get_client_icon():
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            
            body = AnnularSector(
                inner_radius=0, 
                outer_radius=0.5, 
                start_angle=PI, 
                angle=-PI, 
                color=LIGHT_PINK, 
                fill_opacity=1
            )
            body.stretch(1.2, dim=1) 
            body.shift(DOWN * 0.15)
            
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.5)
            spokes = VGroup()
            nodes = VGroup()
            angles = [0, 72, 144, 216, 288] 
            radius = 0.65
            for angle in angles:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * radius, np.sin(rad) * radius, 0])
                spokes.add(Line(start=ORIGIN, end=pos, color=ICON_BASE_COLOR, stroke_width=2))
                nodes.add(Circle(radius=0.08, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(pos))
            network = VGroup(spokes, hub, nodes)
            box = Square(side_length=1.8, color=ICON_BASE_COLOR, stroke_width=2)
            icon_group = VGroup(box, network)
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(icon_group, UP, buff=0.1)
            return VGroup(icon_group, label)

        def get_db_icon():
            front_sq = Square(side_length=0.9, color=ICON_BASE_COLOR)
            back_sq = Square(side_length=0.9, color=ICON_BASE_COLOR).shift(UP*0.25 + RIGHT*0.25)
            connectors = VGroup(
                Line(front_sq.get_corner(UL), back_sq.get_corner(UL), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(UR), back_sq.get_corner(UR), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(DL), back_sq.get_corner(DL), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(DR), back_sq.get_corner(DR), color=ICON_BASE_COLOR),
            )
            dots = VGroup(
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + LEFT*0.15),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(back_sq.get_center() + RIGHT*0.15 + UP*0.1),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + DOWN*0.15 + RIGHT*0.1),
            )
            icon_group = VGroup(back_sq, front_sq, connectors, dots)
            label = Text("Vector Database", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.1)
            return VGroup(icon_group, label)

        def get_llm_icon():
            circle = Circle(radius=0.6, color=ICON_BASE_COLOR, stroke_width=3)
            text = Text("LLM", font_size=24, color=TEXT_COLOR, weight=BOLD).move_to(circle)
            return VGroup(circle, text)

        def get_fine_tuning_icon():
            circle = Circle(radius=0.35, color=ICON_BASE_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            text = Text("Fine\nTuning", font_size=10, color=TEXT_COLOR, line_spacing=1).move_to(circle)
            return VGroup(circle, text)

        def get_content_icons():
            def make_doc(color):
                doc = Rectangle(height=0.5, width=0.35, color=color, stroke_width=1.5)
                corner = Polygon(
                    doc.get_corner(UR), 
                    doc.get_corner(UR)+LEFT*0.12, 
                    doc.get_corner(UR)+DOWN*0.12+LEFT*0.12, 
                    doc.get_corner(UR)+DOWN*0.12, 
                    color=color, stroke_width=1.5, fill_color=BACKGROUND_COLOR, fill_opacity=1
                )
                return VGroup(doc, corner)

            orig_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(6)]).arrange_in_grid(rows=2, buff=0.08)
            new_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(4)]).arrange_in_grid(rows=2, buff=0.08)
            all_docs = VGroup(orig_docs, new_docs).arrange(RIGHT, buff=0.3)
            orig_label = Text("Original Content", font_size=12, color=PRIMARY_COLOR).next_to(orig_docs, DOWN, buff=0.1)
            new_label = Text("New Content", font_size=12, color=PRIMARY_COLOR).next_to(new_docs, DOWN, buff=0.1)
            return VGroup(all_docs, orig_label, new_label)

        def get_number_circle(number):
            circle = Circle(radius=0.15, color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=1)
            num = Text(str(number), color=WHITE, font_size=16, weight=BOLD).move_to(circle)
            return VGroup(circle, num)

        def create_straight_arrow(start_point, end_point, color=ICON_BASE_COLOR):
            line = Line(start=start_point, end=end_point, color=color, stroke_width=3)
            line.add_tip(tip_length=0.2, tip_width=0.2)
            return line

        # --- 2. Layout Positioning ---
        
        # Title
        title = Text("RAG Architecture Model", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)

        # Icons
        framework = get_framework_icon().shift(UP*0.5) 
        client = get_client_icon().next_to(framework, LEFT, buff=2.0).shift(DOWN*0.2)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.0).shift(DOWN*0.2)
        db = get_db_icon().next_to(framework, DOWN, buff=1.5)
        content = get_content_icons().next_to(db, RIGHT, buff=0.8).align_to(db, DOWN)
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        
        ft_connector = DashedLine(
            start=fine_tuning.get_bottom(), 
            end=llm.get_top(), 
            color=ICON_BASE_COLOR, 
            stroke_width=2,
            dash_length=0.1
        )

        # Arrows - using matched Y/X coordinates for perfectly straight arrows
        
        # Horizontal arrows between Client and Framework
        y_level_1 = client[0].get_center()[1]
        arrow_c_f = create_straight_arrow(
            [client[0].get_right()[0] + 0.1, y_level_1, 0],
            [framework[0].get_left()[0] - 0.1, y_level_1, 0],
            color=PRIMARY_COLOR
        )

        y_level_2 = y_level_1 + 0.4
        arrow_f_c = create_straight_arrow(
            [framework[0].get_left()[0] - 0.1, y_level_2, 0],
            [client[0].get_right()[0] + 0.1, y_level_2, 0],
            color=PRIMARY_COLOR
        )

        # Horizontal arrows between Framework and LLM
        y_level_3 = framework[0].get_center()[1]
        arrow_f_llm = create_straight_arrow(
            [framework[0].get_right()[0] + 0.1, y_level_3, 0],
            [llm[0].get_left()[0] - 0.1, y_level_3, 0],
            color=PRIMARY_COLOR
        )

        y_level_4 = y_level_3 + 0.4
        arrow_llm_f = create_straight_arrow(
            [llm[0].get_left()[0] - 0.1, y_level_4, 0],
            [framework[0].get_right()[0] + 0.1, y_level_4, 0],
            color=PRIMARY_COLOR
        )

        # Vertical arrows between Framework and Database
        x_level_1 = framework[0].get_center()[0] - 0.4
        arrow_f_db = create_straight_arrow(
            [x_level_1, framework[0].get_bottom()[1] - 0.1, 0],
            [x_level_1, db[0].get_top()[1] + 0.1, 0],
            color=PRIMARY_COLOR
        )

        x_level_2 = framework[0].get_center()[0] + 0.4
        arrow_db_f = create_straight_arrow(
            [x_level_2, db[0].get_top()[1] + 0.1, 0],
            [x_level_2, framework[0].get_bottom()[1] - 0.1, 0],
            color=PRIMARY_COLOR
        )

        # Horizontal arrow between Content and Database
        y_level_5 = db[0].get_center()[1]
        arrow_content_db = create_straight_arrow(
            [content[0].get_left()[0] - 0.1, y_level_5, 0],
            [db[0].get_right()[0] + 0.1, y_level_5, 0],
            color=ICON_BASE_COLOR
        )

        # Labels & Numbers (Initial State)
        label_q = Text("Question", font_size=16, color=TEXT_COLOR).next_to(arrow_c_f, DOWN, buff=0.1)
        num_1 = get_number_circle(1).next_to(label_q, LEFT, buff=0.1)
        
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR).next_to(arrow_f_c, UP, buff=0.1)
        
        # Bottom Labels (To be faded)
        label_sem = Text("Semantic\nSearch", font_size=14, color=TEXT_COLOR, line_spacing=1).next_to(arrow_f_db, LEFT, buff=0.1)
        num_2 = get_number_circle(2).next_to(label_sem, DOWN, buff=0.1)
        label_ctx = Text("Contextual\nData", font_size=14, color=TEXT_COLOR, line_spacing=1).next_to(arrow_db_f, RIGHT, buff=0.1)
        
        # Right Labels (To be changed)
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR).next_to(arrow_f_llm, DOWN, buff=0.1)
        num_3 = get_number_circle(3).next_to(label_prompt, DOWN, buff=0.1)
        
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).next_to(arrow_llm_f, UP, buff=0.1)
        num_4 = get_number_circle(4).next_to(label_post, UP, buff=0.1)

        # Center Scene
        diagram_group = VGroup(
            client, framework, llm, fine_tuning, ft_connector,
            db, content,
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f, arrow_f_db, arrow_db_f, arrow_content_db,
            label_q, num_1, label_resp, 
            label_sem, num_2, label_ctx, 
            label_prompt, num_3, label_post, num_4
        )
        diagram_group.move_to(ORIGIN)

        # --- 3. Animation Sequence ---
        
        self.add(title, diagram_group)
        self.wait(1.5)

        # Define groups to interact with
        elements_below_framework = VGroup(
            db, content,
            arrow_f_db, arrow_db_f, arrow_content_db,
            label_sem, num_2, label_ctx
        )

        # Create new numbers for the transformation
        # Prompt becomes 2
        new_num_2 = get_number_circle(2).move_to(num_3.get_center())
        # Post Processing becomes 3
        new_num_3 = get_number_circle(3).move_to(num_4.get_center())

        # Animate: Fade out bottom AND Transform numbers simultaneously
        self.play(
            FadeOut(elements_below_framework, shift=DOWN*0.5),
            Transform(num_3, new_num_2),
            Transform(num_4, new_num_3),
            run_time=2.5
        )

        self.wait(2)

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Highlights, Numbers)
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # Black text for white background
ICON_BASE_COLOR = "#ec5599"    # Medium Pink/Grey for icons
BACKGROUND_COLOR = WHITE       # White background
LIGHT_PINK = "#fbcfe8"         # Solid Light Pink for Client

class LLMTransitionScene(Scene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers ---

        def get_client_icon():
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            body = AnnularSector(
                inner_radius=0, outer_radius=0.5, start_angle=PI, angle=-PI, 
                color=LIGHT_PINK, fill_opacity=1
            )
            body.stretch(1.2, dim=1)
            body.shift(DOWN * 0.15)
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.5)
            spokes = VGroup()
            nodes = VGroup()
            angles = [0, 72, 144, 216, 288] 
            radius = 0.65
            for angle in angles:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * radius, np.sin(rad) * radius, 0])
                spokes.add(Line(start=ORIGIN, end=pos, color=ICON_BASE_COLOR, stroke_width=2))
                nodes.add(Circle(radius=0.08, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(pos))
            network = VGroup(spokes, hub, nodes)
            box = Square(side_length=1.8, color=ICON_BASE_COLOR, stroke_width=2)
            icon_group = VGroup(box, network)
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(icon_group, UP, buff=0.1)
            return VGroup(icon_group, label)

        def get_llm_icon():
            circle = Circle(radius=0.6, color=ICON_BASE_COLOR, stroke_width=3, fill_color=WHITE, fill_opacity=1)
            text = Text("LLM", font_size=24, color=TEXT_COLOR, weight=BOLD).move_to(circle)
            return VGroup(circle, text)

        def get_fine_tuning_icon():
            circle = Circle(radius=0.35, color=ICON_BASE_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            text = Text("Fine\nTuning", font_size=10, color=TEXT_COLOR, line_spacing=1).move_to(circle)
            return VGroup(circle, text)

        def create_straight_arrow(start_point, end_point, color=ICON_BASE_COLOR):
            line = Line(start=start_point, end=end_point, color=color, stroke_width=3)
            line.add_tip(tip_length=0.2, tip_width=0.2)
            return line
            
        # --- Helper for target icons ---
        def get_platform_icons():
            # 1. Google Icon (G)
            g_circ = Circle(radius=0.6, color=PRIMARY_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            g_text = Text("G", font_size=40, weight=BOLD, color=PRIMARY_COLOR).move_to(g_circ)
            google = VGroup(g_circ, g_text)
            
            # 2. Wikipedia Icon (W)
            w_circ = Circle(radius=0.6, color=PRIMARY_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            w_text = Text("W", font_size=40, font="serif", weight=BOLD, color=PRIMARY_COLOR).move_to(w_circ)
            wiki = VGroup(w_circ, w_text)
            
            # 3. Bank Info Icon ($) - Replaces Facebook
            b_circ = Circle(radius=0.6, color=PRIMARY_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            b_text = Text("$", font_size=40, weight=BOLD, color=PRIMARY_COLOR).move_to(b_circ)
            bank = VGroup(b_circ, b_text)
            
            # 4. YouTube Icon (Play Triangle only)
            y_circ = Circle(radius=0.6, color=PRIMARY_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            tri = Triangle(color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=1).scale(0.25).rotate(-90*DEGREES).move_to(y_circ).shift(RIGHT*0.05)
            youtube = VGroup(y_circ, tri)

            # Labels
            labels = ["Google", "Wikipedia", "Bank Info", "YouTube"]
            icons = [google, wiki, bank, youtube]
            
            final_group = VGroup()
            for icon, label_text in zip(icons, labels):
                l = Text(label_text, font_size=16, color=TEXT_COLOR).next_to(icon, DOWN, buff=0.2)
                final_group.add(VGroup(icon, l))
                
            return final_group

        # --- 2. Initial State Setup ---
        
        title = Text("RAG Architecture Model", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)
        
        framework = get_framework_icon().shift(UP*0.5) 
        client = get_client_icon().next_to(framework, LEFT, buff=2.0).shift(DOWN*0.2)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.0).shift(DOWN*0.2)
        
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        ft_connector = DashedLine(start=fine_tuning.get_bottom(), end=llm.get_top(), color=ICON_BASE_COLOR, stroke_width=2)

        # Arrows - using matched Y/X coordinates for perfectly straight arrows
        
        # Horizontal arrows between Client and Framework
        y_level_1 = client[0].get_center()[1]
        arrow_c_f = create_straight_arrow(
            [client[0].get_right()[0] + 0.1, y_level_1, 0],
            [framework[0].get_left()[0] - 0.1, y_level_1, 0],
            color=PRIMARY_COLOR
        )

        y_level_2 = y_level_1 + 0.4
        arrow_f_c = create_straight_arrow(
            [framework[0].get_left()[0] - 0.1, y_level_2, 0],
            [client[0].get_right()[0] + 0.1, y_level_2, 0],
            color=PRIMARY_COLOR
        )

        # Horizontal arrows between Framework and LLM
        y_level_3 = framework[0].get_center()[1]
        arrow_f_llm = create_straight_arrow(
            [framework[0].get_right()[0] + 0.1, y_level_3, 0],
            [llm[0].get_left()[0] - 0.1, y_level_3, 0],
            color=PRIMARY_COLOR
        )

        y_level_4 = y_level_3 + 0.4
        arrow_llm_f = create_straight_arrow(
            [llm[0].get_left()[0] - 0.1, y_level_4, 0],
            [framework[0].get_right()[0] + 0.1, y_level_4, 0],
            color=PRIMARY_COLOR
        )

        label_q = Text("Question", font_size=16, color=TEXT_COLOR).next_to(arrow_c_f, DOWN, buff=0.1)
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR).next_to(arrow_f_c, UP, buff=0.1)
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR).next_to(arrow_f_llm, DOWN, buff=0.1)
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).next_to(arrow_llm_f, UP, buff=0.1)
        
        # Group everything for the initial view (No DB here)
        diagram_group = VGroup(
            client, framework, llm, fine_tuning, ft_connector,
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f,
            label_q, label_resp, label_prompt, label_post
        )
        diagram_group.move_to(ORIGIN)

        self.add(title, diagram_group)
        self.wait(1)

        # --- 3. Animation Sequence ---

        # 1. Fade out everything except Client and LLM
        items_to_fade = VGroup(
            title, framework, fine_tuning, ft_connector,
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f,
            label_q, label_resp, label_prompt, label_post
        )

        self.play(FadeOut(items_to_fade), run_time=1.5)

        # 2. Layout new positions
        # Create Question Box
        q_text = "Question: I work remotely. Can I expense a\n$1,200 monitor that I use for my work?"
        q_box = Rectangle(height=1.5, width=4.5, color=ICON_BASE_COLOR, fill_color=LIGHT_PINK, fill_opacity=0.2)
        q_content = Text(q_text, font_size=16, color=TEXT_COLOR, line_spacing=1.2).move_to(q_box)
        q_group = VGroup(q_box, q_content)
        
        # Create a temporary centered group to calculate positions
        # Client on Left, Question on Right
        temp_top_group = VGroup(client.copy(), q_group.copy()).arrange(RIGHT, buff=0.5)
        temp_top_group.move_to(UP * 2.5)
        
        target_client_pos = temp_top_group[0].get_center()
        target_q_pos = temp_top_group[1].get_center()
        
        # Set question box to its final position (hidden)
        q_group.move_to(target_q_pos)

        # Move Client to target and LLM to Center Screen
        self.play(
            client.animate.move_to(target_client_pos),
            llm.animate.move_to(ORIGIN + DOWN * 0.5), 
            run_time=2.0
        )
        
        # Fade in Question next to client
        self.play(FadeIn(q_group, shift=LEFT), run_time=1.0)
        self.wait(0.5)

        # 3. Create the 4 Icons Group (hidden initially)
        platform_icons = get_platform_icons()
        # Arrange in 1x4 grid
        platform_icons.arrange(RIGHT, buff=0.6)
        # Center them on screen (where LLM is, roughly)
        platform_icons.move_to(llm.get_center())
        
        # Prepare LLM copies for splitting animation
        llm_copies = VGroup(*[llm.copy() for _ in range(4)])
        llm_copies.move_to(llm.get_center())
        
        # Swap original LLM with copies
        self.remove(llm)
        self.add(llm_copies)
        
        # Move copies to the positions of the 4 platform icons
        anims = []
        for i in range(4):
            anims.append(llm_copies[i].animate.move_to(platform_icons[i].get_center()))
            
        self.play(*anims, run_time=1.5, rate_func=smooth)
        
        # Morph copies into the actual icons
        morph_anims = []
        for i in range(4):
            morph_anims.append(ReplacementTransform(llm_copies[i], platform_icons[i]))
            
        self.play(*morph_anims, run_time=2.0, rate_func=smooth)
        
        self.wait(3)

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Highlights, Key Objects)
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink (Background accents)
ACCENT_COLOR = "#be185d"       # Darker pink for emphasis
TEXT_COLOR = BLACK             # Black text
ICON_BASE_COLOR = "#ec5599"    # Medium Pink/Grey for standard icons
BACKGROUND_COLOR = WHITE       # White background
LIGHT_PINK = "#fbcfe8"         # Solid Light Pink for Client fill
DATA_COLOR = "#95114c"         # Blue for "New Data" to distinguish updates
OUTDATED_COLOR = "#5B273E"     # Gray for outdated model

class FineTuningInefficiency(Scene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Generators ---

        def get_client_icon():
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            body = AnnularSector(
                inner_radius=0, outer_radius=0.5, start_angle=PI, angle=-PI, 
                color=LIGHT_PINK, fill_opacity=1
            )
            body.stretch(1.2, dim=1)
            body.shift(DOWN * 0.15)
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.5)
            spokes = VGroup()
            nodes = VGroup()
            angles = [0, 72, 144, 216, 288] 
            radius = 0.65
            for angle in angles:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * radius, np.sin(rad) * radius, 0])
                spokes.add(Line(start=ORIGIN, end=pos, color=ICON_BASE_COLOR, stroke_width=2))
                nodes.add(Circle(radius=0.08, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(pos))
            network = VGroup(spokes, hub, nodes)
            box = Square(side_length=1.8, color=ICON_BASE_COLOR, stroke_width=2)
            icon_group = VGroup(box, network)
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(icon_group, UP, buff=0.1)
            return VGroup(icon_group, label)

        def get_llm_icon(label_text="LLM", stroke_color=ICON_BASE_COLOR):
            circle = Circle(radius=0.75, color=stroke_color, stroke_width=4, fill_color=WHITE, fill_opacity=1)
            font_s = 20 if len(label_text) > 5 else 24
            text = Text(label_text, font_size=font_s, color=TEXT_COLOR, weight=BOLD, line_spacing=1).move_to(circle)
            group = VGroup(circle, text)
            group.set_z_index(10) 
            return group

        def get_fine_tuning_icon():
            circle = Circle(radius=0.45, color=ICON_BASE_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            text = Text("Fine\nTuning", font_size=12, color=TEXT_COLOR, line_spacing=1).move_to(circle)
            group = VGroup(circle, text)
            group.set_z_index(10)
            return group

        def get_document_icon(color=PRIMARY_COLOR):
            doc = Rectangle(height=0.6, width=0.45, color=color, fill_color=WHITE, fill_opacity=1, stroke_width=2)
            lines = VGroup(*[Line(start=LEFT*0.12, end=RIGHT*0.12, color=color, stroke_width=1.5).shift(UP*0.1 - i*0.1) for i in range(3)])
            lines.move_to(doc.get_center())
            return VGroup(doc, lines)

        def create_straight_arrow(start_point, end_point, color=ICON_BASE_COLOR):
            line = Line(start=start_point, end=end_point, color=color, stroke_width=3)
            line.add_tip(tip_length=0.2, tip_width=0.2)
            return line

        # --- PART 1: The Initial Scene (RAG Model) ---
        
        title = Text("RAG Architecture Model", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)
        
        framework = get_framework_icon().shift(UP*0.5) 
        client = get_client_icon().next_to(framework, LEFT, buff=2.0).shift(DOWN*0.2)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.0).shift(DOWN*0.2)
        
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        ft_connector = DashedLine(start=fine_tuning.get_bottom(), end=llm.get_top(), color=ICON_BASE_COLOR, stroke_width=2)

        # Arrows - using matched Y/X coordinates for perfectly straight arrows
        y_level_1 = client[0].get_center()[1]
        arrow_c_f = create_straight_arrow(
            [client[0].get_right()[0] + 0.1, y_level_1, 0],
            [framework[0].get_left()[0] - 0.1, y_level_1, 0],
            color=PRIMARY_COLOR
        )

        y_level_2 = y_level_1 + 0.4
        arrow_f_c = create_straight_arrow(
            [framework[0].get_left()[0] - 0.1, y_level_2, 0],
            [client[0].get_right()[0] + 0.1, y_level_2, 0],
            color=PRIMARY_COLOR
        )

        y_level_3 = framework[0].get_center()[1]
        arrow_f_llm = create_straight_arrow(
            [framework[0].get_right()[0] + 0.1, y_level_3, 0],
            [llm[0].get_left()[0] - 0.1, y_level_3, 0],
            color=PRIMARY_COLOR
        )

        y_level_4 = y_level_3 + 0.4
        arrow_llm_f = create_straight_arrow(
            [llm[0].get_left()[0] - 0.1, y_level_4, 0],
            [framework[0].get_right()[0] + 0.1, y_level_4, 0],
            color=PRIMARY_COLOR
        )

        label_q = Text("Question", font_size=16, color=TEXT_COLOR).next_to(arrow_c_f, DOWN, buff=0.1)
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR).next_to(arrow_f_c, UP, buff=0.1)
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR).next_to(arrow_f_llm, DOWN, buff=0.1)
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).next_to(arrow_llm_f, UP, buff=0.1)
        
        # Draw Initial State
        self.add(title, client, framework, llm, fine_tuning, ft_connector, arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f, label_q, label_resp, label_prompt, label_post)
        self.wait(1.5)

        # --- PART 2: The Transition (Fade to Focus) ---
        
        fade_group = VGroup(
            title, framework, ft_connector,
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f,
            label_q, label_resp, label_prompt, label_post
        )
        
        self.play(FadeOut(fade_group), run_time=1.0)
        
        # New Title
        ft_title = Text("Fine Tuning: The Process & Cost", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)
        self.play(Write(ft_title))

        # Re-positioning: Client Left, Fine Tuning Center, LLM Right
        target_client_pos = LEFT * 5
        target_ft_pos = ORIGIN
        target_llm_pos = RIGHT * 4
        
        self.play(
            client.animate.move_to(target_client_pos),
            fine_tuning.animate.scale(1.5).move_to(target_ft_pos), 
            llm.animate.move_to(target_llm_pos),
            run_time=1.5
        )
        
        base_model_label = Text("", font_size=16, color=OUTDATED_COLOR).next_to(llm, DOWN)
        self.play(FadeIn(base_model_label))
        self.wait(1)

        # --- PART 3: The "Temptation" (Organization Data) ---
        
        org_data = VGroup(*[get_document_icon().shift(RIGHT*i*0.15 + DOWN*i*0.15) for i in range(3)])
        org_data.next_to(client, RIGHT, buff=0.5)
        
        data_label = Text("Organization Data", font_size=14, color=PRIMARY_COLOR).next_to(org_data, UP, buff=0.1)
        
        self.play(FadeIn(org_data, shift=UP), Write(data_label))
        
        # Animation: Data flows INTO (and BEHIND) Fine Tuning
        moving_docs = org_data.copy()
        
        self.play(
            moving_docs.animate.move_to(fine_tuning.get_center()),
            run_time=1.5
        )
        self.remove(moving_docs)
        
        # Animation: Processed info moves to LLM
        processed_stream = Line(start=fine_tuning.get_right(), end=llm.get_left(), color=PRIMARY_COLOR, stroke_width=5)
        processed_stream.set_z_index(0) 
        
        self.play(Create(processed_stream))
        
        # Transform LLM to "Custom Model"
        custom_llm = get_llm_icon("Custom\nModel", stroke_color=PRIMARY_COLOR)
        custom_llm.move_to(llm.get_center())
        
        self.play(
            ReplacementTransform(llm, custom_llm),
            processed_stream.animate.set_stroke(opacity=0.2)
        )
        
        success_text = Text("Knowledge Integrated", font_size=14, color=PRIMARY_COLOR).next_to(custom_llm, UP)
        self.play(Write(success_text))
        self.wait(1)

        # --- PART 4: The Problem (Updates & Inefficiency) ---
        
        # 1. Update the content (Data changes to BLUE)
        new_data_label = Text("Updated Content!", font_size=16, color=DATA_COLOR, weight=BOLD).next_to(client, UP, buff=0.5)
        new_org_data = VGroup(*[get_document_icon(color=DATA_COLOR).shift(RIGHT*i*0.15 + DOWN*i*0.15) for i in range(3)])
        new_org_data.move_to(org_data.get_center())
        
        self.play(
            Transform(org_data, new_org_data),
            Transform(data_label, new_data_label),
            Flash(org_data, color=DATA_COLOR)
        )
        
        # 2. Show that model is OUTDATED
        outdated_llm = get_llm_icon("Custom\nModel", stroke_color=OUTDATED_COLOR)
        outdated_llm.move_to(custom_llm.get_center())
        
        self.play(
            ReplacementTransform(custom_llm, outdated_llm),
            FadeOut(success_text)
        )
        
        warning = Text("Model is now outdated", font_size=14, color=ACCENT_COLOR).next_to(outdated_llm, UP)
        self.play(Write(warning))
        self.wait(0.5)
        
        # 3. Show bullet points instead of animation
        bullet_1 = Text("1. Fine tuning on updated data is impractical.", font_size=20, color=TEXT_COLOR).to_edge(DOWN, buff=2.0).to_edge(LEFT, buff=1.0)
        bullet_2 = Text("2. Retraining the model is cost intensive.", font_size=20, color=TEXT_COLOR).next_to(bullet_1, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.play(Write(bullet_1))
        self.wait(0.5)
        self.play(Write(bullet_2))
        
        self.wait(3)

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Highlights, Numbers)
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # Black text for white background
ICON_BASE_COLOR = "#ec5599"    # Dark Grey/Pinkish base
BACKGROUND_COLOR = WHITE       # White background
LIGHT_PINK = "#fbcfe8"
BLUE_COLOR = "#3b82f6"         # Solid Light Blue for Context/Relevant Docs

class RAGArchitectureSceneGood(Scene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers ---

        def get_client_icon():
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            
            body = AnnularSector(
                inner_radius=0, 
                outer_radius=0.5, 
                start_angle=PI, 
                angle=-PI, 
                color=LIGHT_PINK, 
                fill_opacity=1
            )
            body.stretch(1.2, dim=1) 
            body.shift(DOWN * 0.15)
            
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            box = Square(side_length=2.8, color=ICON_BASE_COLOR, stroke_width=2.5)
            
            sys_text = Paragraph(
                "System prompt = e.g.",
                "You are a digital assistant",
                "for our organization...",
                alignment="center",
                font_size=12,
                color=TEXT_COLOR
            )
            
            user_text = Text(
                "User prompt (Question)\n\nMost relevant documents", 
                font_size=12, 
                color=PRIMARY_COLOR, 
                weight=BOLD,
                t2c={"Most relevant documents": BLUE_COLOR} 
            )
            
            text_group = VGroup(sys_text, user_text).arrange(DOWN, buff=0.2)
            text_group.move_to(box.get_center())
            
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(box, UP, buff=0.1)
            return VGroup(box, text_group, label)

        def get_question_bubble():
            q_str = "Question: I work remotely. Can I\nexpense a $1,200 monitor that\nI use for my work?"
            text = Text(q_str, font_size=12, color=TEXT_COLOR, line_spacing=1.2)
            
            box = RoundedRectangle(
                corner_radius=0.2, 
                height=text.height + 0.4, 
                width=text.width + 0.4, 
                color=PRIMARY_COLOR, 
                stroke_width=2,
                fill_color=WHITE, 
                fill_opacity=1
            )
            text.move_to(box)
            return VGroup(box, text)

        def get_response_bubble():
            r_str = "Response: No, you cannot expense a $1,200 monitor\nbecause there is a temporary pause on\nreimbursement requests for computer\nmonitors exceeding $800."
            text = Text(r_str, font_size=12, color=TEXT_COLOR, line_spacing=1.2, slant=ITALIC)
            
            box = RoundedRectangle(
                corner_radius=0.2, 
                height=text.height + 0.4, 
                width=text.width + 0.4, 
                color=PRIMARY_COLOR, 
                stroke_width=2,
                fill_color=LIGHT_PINK, 
                fill_opacity=0.3
            )
            text.move_to(box)
            return VGroup(box, text)

        def get_db_icon():
            front_sq = Square(side_length=0.9, color=ICON_BASE_COLOR)
            back_sq = Square(side_length=0.9, color=ICON_BASE_COLOR).shift(UP*0.25 + RIGHT*0.25)
            connectors = VGroup(
                Line(front_sq.get_corner(UL), back_sq.get_corner(UL), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(UR), back_sq.get_corner(UR), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(DL), back_sq.get_corner(DL), color=ICON_BASE_COLOR),
                Line(front_sq.get_corner(DR), back_sq.get_corner(DR), color=ICON_BASE_COLOR),
            )
            dots = VGroup(
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + LEFT*0.15),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(back_sq.get_center() + RIGHT*0.15 + UP*0.1),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + DOWN*0.15 + RIGHT*0.1),
            )
            icon_group = VGroup(back_sq, front_sq, connectors, dots)
            label = Text("Vector Database", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.1)
            return VGroup(icon_group, label)

        def get_llm_icon():
            circle = Circle(radius=0.6, color=ICON_BASE_COLOR, stroke_width=3)
            text = Text("LLM", font_size=24, color=TEXT_COLOR, weight=BOLD).move_to(circle)
            return VGroup(circle, text)

        def get_fine_tuning_icon():
            circle = Circle(radius=0.35, color=ICON_BASE_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            text = Text("Fine\nTuning", font_size=10, color=TEXT_COLOR, line_spacing=1).move_to(circle)
            return VGroup(circle, text)

        def get_content_icons():
            def make_doc(color):
                doc = Rectangle(height=0.5, width=0.35, color=color, stroke_width=1.5)
                corner = Polygon(
                    doc.get_corner(UR), 
                    doc.get_corner(UR)+LEFT*0.12, 
                    doc.get_corner(UR)+DOWN*0.12+LEFT*0.12, 
                    doc.get_corner(UR)+DOWN*0.12, 
                    color=color, stroke_width=1.5, fill_color=BACKGROUND_COLOR, fill_opacity=1
                )
                return VGroup(doc, corner)

            orig_docs = VGroup(*[make_doc(BLUE_COLOR) for _ in range(6)]).arrange_in_grid(rows=2, buff=0.08)
            new_docs = VGroup(*[make_doc(BLUE_COLOR) for _ in range(4)]).arrange_in_grid(rows=2, buff=0.08)
            all_docs = VGroup(orig_docs, new_docs).arrange(RIGHT, buff=0.3)
            orig_label = Text("Top N most", font_size=12, color=BLUE_COLOR).next_to(orig_docs, DOWN, buff=0.1)
            new_label = Text("relevant documents", font_size=12, color=BLUE_COLOR).next_to(new_docs, DOWN, buff=0.1)
            return VGroup(all_docs, orig_label, new_label)

        def get_number_circle(number):
            circle = Circle(radius=0.15, color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=1)
            num = Text(str(number), color=WHITE, font_size=16, weight=BOLD).move_to(circle)
            return VGroup(circle, num)

        def create_straight_arrow(start_point, end_point, color=ICON_BASE_COLOR):
            line = Line(start=start_point, end=end_point, color=color, stroke_width=3)
            line.add_tip(tip_length=0.2, tip_width=0.2)
            return line

        # --- 2. Layout Positioning ---
        
        framework = get_framework_icon().shift(UP*0.5) 
        client = get_client_icon().next_to(framework, LEFT, buff=2.5).shift(UP*0.5)
        
        question_bubble = get_question_bubble().next_to(client, DOWN, buff=0.5)
        response_bubble = get_response_bubble().next_to(question_bubble, DOWN, buff=0.2)
        
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.0).shift(DOWN*0.2)
        db = get_db_icon().next_to(framework, DOWN, buff=1.8)
        content = get_content_icons().next_to(db, RIGHT, buff=1.0).align_to(db, DOWN)
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        ft_connector = DashedLine(
            start=fine_tuning.get_bottom(), 
            end=llm.get_top(), 
            color=ICON_BASE_COLOR, 
            stroke_width=2,
            dash_length=0.1
        )

        initial_group = VGroup(client, framework, llm, fine_tuning, ft_connector)
        scene_center = VGroup(initial_group, db, content, question_bubble, response_bubble).get_center()
        
        all_objects = VGroup(client, framework, llm, db, content, fine_tuning, ft_connector, question_bubble, response_bubble)
        all_objects.shift(-scene_center)

        # Arrows - using matched Y/X coordinates for perfectly straight arrows
        
        # Horizontal arrows between Client and Framework
        y_level_1 = client[0].get_center()[1] - 0.2
        arrow_c_f = create_straight_arrow(
            [client[0].get_right()[0] + 0.1, y_level_1, 0],
            [framework[0].get_left()[0] - 0.1, y_level_1, 0]
        )
        
        y_level_2 = client[0].get_center()[1] + 0.5
        arrow_f_c = create_straight_arrow(
            [framework[0].get_left()[0] - 0.1, y_level_2, 0],
            [client[0].get_right()[0] + 0.1, y_level_2, 0]
        )
        
        # Horizontal arrows between Framework and LLM
        y_level_3 = framework[0].get_center()[1] - 0.2
        arrow_f_llm = create_straight_arrow(
            [framework[0].get_right()[0] + 0.1, y_level_3, 0],
            [llm[0].get_left()[0] - 0.1, y_level_3, 0]
        )
        
        y_level_4 = framework[0].get_center()[1] + 0.6
        arrow_llm_f = create_straight_arrow(
            [llm[0].get_left()[0] - 0.1, y_level_4, 0],
            [framework[0].get_right()[0] + 0.1, y_level_4, 0]
        )
        
        # Vertical arrows between Framework and Database
        x_level_1 = framework[0].get_center()[0] - 0.5
        arrow_f_db = create_straight_arrow(
            [x_level_1, framework[0].get_bottom()[1] - 0.1, 0],
            [x_level_1, db[0].get_top()[1] + 0.1, 0]
        )
        
        x_level_2 = framework[0].get_center()[0] + 0.5
        arrow_db_f = create_straight_arrow(
            [x_level_2, db[0].get_top()[1] + 0.1, 0],
            [x_level_2, framework[0].get_bottom()[1] - 0.1, 0]
        )
        
        # Horizontal arrow between Content and Database
        y_level_5 = db[0].get_center()[1]
        arrow_content_db = create_straight_arrow(
            [content[0].get_left()[0] - 0.1, y_level_5, 0],
            [db[0].get_right()[0] + 0.1, y_level_5, 0]
        )

        # Labels
        label_q = Text("Question", font_size=16, color=TEXT_COLOR, slant=ITALIC)
        label_q.move_to(arrow_c_f.get_center()).shift(DOWN * 0.25)
        
        num_1 = get_number_circle(1).next_to(label_q, LEFT, buff=0.1)
        
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR, slant=ITALIC)
        label_resp.move_to(arrow_f_c.get_center()).shift(UP * 0.25)
        
        label_sem = Text("Semantic\nSearch", font_size=14, color=TEXT_COLOR, line_spacing=1)
        label_sem.move_to(arrow_f_db.get_center()).shift(LEFT * 0.6) 
        
        num_2 = get_number_circle(2).next_to(label_sem, DOWN, buff=0.1)
        
        label_ctx = Text("Contextual\nData", font_size=14, color=BLUE_COLOR, line_spacing=1)
        label_ctx.move_to(arrow_db_f.get_center()).shift(RIGHT * 0.6) 
        
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR)
        label_prompt.move_to(arrow_f_llm.get_center()).shift(DOWN * 0.25)
        
        num_3 = get_number_circle(3).next_to(label_prompt, DOWN, buff=0.1)
        
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR)
        label_post.move_to(arrow_llm_f.get_center()).shift(UP * 0.25)
        
        num_4 = get_number_circle(4).next_to(label_post, UP, buff=0.1)

        # --- 3. Animation Sequence ---
        
        self.play(
            LaggedStart(
                FadeIn(client), FadeIn(framework), FadeIn(llm), 
                FadeIn(fine_tuning), Create(ft_connector),
                lag_ratio=0.1
            ), run_time=1.5
        )
        self.wait(0.5)

        # Phase 1: Question
        self.play(Write(question_bubble))
        self.wait(0.5)
        
        arrow_c_f.set_color(PRIMARY_COLOR)
        self.play(Create(arrow_c_f), Write(label_q), FadeIn(num_1))
        self.wait(0.5)

        # Phase 2: Retrieval
        arrow_f_db.set_color(PRIMARY_COLOR)
        self.play(Create(arrow_f_db), Write(label_sem), FadeIn(num_2))
        self.play(FadeIn(db))
        self.play(FadeIn(content))
        self.play(Create(arrow_content_db))
        self.wait(0.5)
        
        arrow_db_f.set_color(BLUE_COLOR)
        self.play(Create(arrow_db_f), Write(label_ctx))
        self.wait(0.5)

        # Phase 3: Prompt
        arrow_f_llm.set_color(PRIMARY_COLOR)
        self.play(Create(arrow_f_llm), Write(label_prompt), FadeIn(num_3))
        self.wait(0.5)

        # Phase 4: Response
        arrow_llm_f.set_color(PRIMARY_COLOR)
        arrow_f_c.set_color(PRIMARY_COLOR)
        
        self.play(Create(arrow_llm_f), Write(label_post), FadeIn(num_4))
        self.play(Create(arrow_f_c), Write(label_resp))
        
        # Final Response
        self.wait(0.5)
        self.play(Write(response_bubble), run_time=1.5)

        self.wait(3)

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"       # Pinkish-Red (Highlights, Key Objects)
SECONDARY_COLOR = "#fce7f3"     # Very Light Pink (Background accents)
ACCENT_COLOR = "#be185d"        # Darker pink for emphasis/warnings
TEXT_COLOR = BLACK              # Black text
ICON_BASE_COLOR = "#ec5599"     # Medium Pink/Grey for standard icons
BACKGROUND_COLOR = WHITE        # White background
LIGHT_PINK = "#fbcfe8"          # Solid Light Pink for Client fill

class HallucinationFocus(Scene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Generators ---

        def get_client_icon():
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            body = AnnularSector(
                inner_radius=0, outer_radius=0.5, start_angle=PI, angle=-PI, 
                color=LIGHT_PINK, fill_opacity=1
            )
            body.stretch(1.2, dim=1)
            body.shift(DOWN * 0.15)
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.5)
            spokes = VGroup()
            nodes = VGroup()
            angles = [0, 72, 144, 216, 288] 
            radius = 0.65
            for angle in angles:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * radius, np.sin(rad) * radius, 0])
                spokes.add(Line(start=ORIGIN, end=pos, color=ICON_BASE_COLOR, stroke_width=2))
                nodes.add(Circle(radius=0.08, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(pos))
            network = VGroup(spokes, hub, nodes)
            box = Square(side_length=1.8, color=ICON_BASE_COLOR, stroke_width=2)
            icon_group = VGroup(box, network)
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(icon_group, UP, buff=0.1)
            return VGroup(icon_group, label)

        def get_llm_icon(label_text="LLM", stroke_color=ICON_BASE_COLOR):
            circle = Circle(radius=0.75, color=stroke_color, stroke_width=4, fill_color=WHITE, fill_opacity=1)
            font_s = 24
            text = Text(label_text, font_size=font_s, color=TEXT_COLOR, weight=BOLD, line_spacing=1).move_to(circle)
            group = VGroup(circle, text)
            group.set_z_index(10) 
            return group

        def create_straight_arrow(start_point, end_point, color=ICON_BASE_COLOR):
            line = Line(start=start_point, end=end_point, color=color, stroke_width=3)
            line.add_tip(tip_length=0.2, tip_width=0.2)
            return line

        def get_chat_interface():
            # Chat interface container
            chat_bg = RoundedRectangle(
                corner_radius=0.2,
                height=4.5,
                width=6,
                color=ICON_BASE_COLOR,
                stroke_width=2,
                fill_color=WHITE,
                fill_opacity=1
            )
            
            # Header bar
            header = Rectangle(
                height=0.5,
                width=6,
                color=ICON_BASE_COLOR,
                fill_color=ICON_BASE_COLOR,
                fill_opacity=1,
                stroke_width=0
            ).align_to(chat_bg, UP)
            
            header_text = Text("ChatGPT", font_size=18, color=WHITE, weight=BOLD)
            header_text.move_to(header.get_center())
            
            # User message bubble (right-aligned)
            user_msg_text = Text(
                "I work remotely. Can I expense\na $1,200 monitor that I use\nfor my work?",
                font_size=14,
                color=TEXT_COLOR,
                line_spacing=1.2
            )
            user_bubble = RoundedRectangle(
                corner_radius=0.15,
                height=user_msg_text.height + 0.3,
                width=user_msg_text.width + 0.4,
                color=PRIMARY_COLOR,
                stroke_width=1.5,
                fill_color=PRIMARY_COLOR,
                fill_opacity=0.2
            )
            user_msg_text.move_to(user_bubble)
            user_msg = VGroup(user_bubble, user_msg_text)
            user_msg.next_to(chat_bg.get_top(), DOWN, buff=1.0)
            user_msg.shift(RIGHT * 1.2)
            
            # AI response bubble (left-aligned)
            ai_msg_text = Text(
                "That's great! Yes, you can definitely\nexpense a $1,200 monitor for your\nremote work setup. This is typically\nconsidered a reasonable work expense.",
                font_size=14,
                color=TEXT_COLOR,
                line_spacing=1.2
            )
            ai_bubble = RoundedRectangle(
                corner_radius=0.15,
                height=ai_msg_text.height + 0.3,
                width=ai_msg_text.width + 0.4,
                color=ACCENT_COLOR,
                stroke_width=1.5,
                fill_color=SECONDARY_COLOR,
                fill_opacity=0.8
            )
            ai_msg_text.move_to(ai_bubble)
            ai_msg = VGroup(ai_bubble, ai_msg_text)
            ai_msg.next_to(user_msg, DOWN, buff=0.5)
            ai_msg.shift(LEFT * 1.2)
            
            chat_content = VGroup(header, header_text, user_msg, ai_msg)
            return VGroup(chat_bg, chat_content)

        # =========================================
        # PHASE 1: The Initial Full Diagram (RAG)
        # =========================================
        
        title = Text("Standard RAG Architecture", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)
        
        framework = get_framework_icon()
        client = get_client_icon().next_to(framework, LEFT, buff=2.5)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.5)
        
        # Arrows - using matched Y/X coordinates for perfectly straight arrows
        y_level_1 = client[0].get_center()[1]
        arrow_c_f = create_straight_arrow(
            [client[0].get_right()[0] + 0.1, y_level_1, 0],
            [framework[0].get_left()[0] - 0.1, y_level_1, 0],
            color=PRIMARY_COLOR
        )
        
        y_level_2 = y_level_1 + 0.4
        arrow_f_c = create_straight_arrow(
            [framework[0].get_left()[0] - 0.1, y_level_2, 0],
            [client[0].get_right()[0] + 0.1, y_level_2, 0],
            color=PRIMARY_COLOR
        )
        
        y_level_3 = framework[0].get_center()[1]
        arrow_f_llm = create_straight_arrow(
            [framework[0].get_right()[0] + 0.1, y_level_3, 0],
            [llm[0].get_left()[0] - 0.1, y_level_3, 0],
            color=PRIMARY_COLOR
        )
        
        y_level_4 = y_level_3 + 0.4
        arrow_llm_f = create_straight_arrow(
            [llm[0].get_left()[0] - 0.1, y_level_4, 0],
            [framework[0].get_right()[0] + 0.1, y_level_4, 0],
            color=PRIMARY_COLOR
        )

        
        label_q = Text("Question", font_size=16, color=TEXT_COLOR).next_to(arrow_c_f, DOWN, buff=0.1)
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR).next_to(arrow_f_c, UP, buff=0.1)
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR, line_spacing=1).next_to(arrow_f_llm, DOWN, buff=0.1)
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).next_to(arrow_llm_f, UP, buff=0.1)

      
        initial_scene_group = VGroup(
            title, client, framework, llm, 
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f, 
            label_q, label_resp, label_prompt, label_post
        )
        
        self.play(FadeIn(initial_scene_group, lag_ratio=0.1))
        self.wait(2)

        # =========================================
        # PHASE 2: Isolate Elements & Show Hallucination
        # =========================================

        elements_to_fade = VGroup(
            title, framework,
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f,
            label_q, label_resp, label_prompt, label_post
        )

        self.play(FadeOut(elements_to_fade), run_time=1.5)

        # Reposition Client and LLM (further apart to avoid touching chat interface)
        target_client_pos = LEFT * 5
        target_llm_pos = RIGHT * 5

        self.play(
            client.animate.move_to(target_client_pos),
            llm.animate.move_to(target_llm_pos),
            run_time=1.5
        )
        self.wait(0.5)

        # Show chat interface
        chat_interface = get_chat_interface()
        chat_interface.move_to(ORIGIN).shift(DOWN * 0.3)
        
        self.play(FadeIn(chat_interface[0]))  # Background
        self.wait(0.3)
        self.play(FadeIn(chat_interface[1][0:2]))  # Header
        self.wait(0.3)
        self.play(Write(chat_interface[1][2]))  # User message
        self.wait(0.5)
        self.play(Write(chat_interface[1][3]))  # AI response
        self.wait(1)

        # Introduce "Hallucination" warning
        hallucination_text = Text("Hallucination", font_size=36, color=ACCENT_COLOR, weight=BOLD)
        hallucination_text.to_edge(UP, buff=0.8)

        self.play(Write(hallucination_text))
        self.play(
            hallucination_text.animate.scale(1.2),
            run_time=0.4,
            rate_func=there_and_back
        )

        # Add warning icon or cross mark on the AI response
        warning_mark = Text("✗", font_size=48, color=ACCENT_COLOR, weight=BOLD)
        warning_mark.move_to(chat_interface[1][3].get_center())
        
        self.play(
            chat_interface[1][3].animate.set_opacity(0.3),
            FadeIn(warning_mark, scale=0.5),
            run_time=1
        )

        self.wait(3)