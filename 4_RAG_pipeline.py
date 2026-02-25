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

        # Arrows
        arrow_c_f = create_straight_arrow(client[0].get_right() + RIGHT*0.1, framework[0].get_left() + LEFT*0.1)
        arrow_f_c = create_straight_arrow(framework[0].get_left() + LEFT*0.1 + UP*0.4, client[0].get_right() + RIGHT*0.1 + UP*0.4)
        arrow_f_llm = create_straight_arrow(framework[0].get_right() + RIGHT*0.1, llm[0].get_left() + LEFT*0.1)
        arrow_llm_f = create_straight_arrow(llm[0].get_left() + LEFT*0.1 + UP*0.4, framework[0].get_right() + RIGHT*0.1 + UP*0.4)
        arrow_f_db = create_straight_arrow(framework[0].get_bottom() + LEFT*0.4 + DOWN*0.1, db[0].get_top() + LEFT*0.4 + UP*0.1)
        arrow_db_f = create_straight_arrow(db[0].get_top() + RIGHT*0.4 + UP*0.1, framework[0].get_bottom() + RIGHT*0.4 + DOWN*0.1)
        arrow_content_db = create_straight_arrow(content[0].get_left() + LEFT*0.1, db[0].get_right() + RIGHT*0.1)

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
        # Removed Circumscribe(db[0])
        self.wait(0.5)

        # Phase 1: Question
        arrow_c_f.set_color(PRIMARY_COLOR)
        self.play(Create(arrow_c_f), Write(label_q), FadeIn(num_1))
        # Removed Circumscribe(client) and Circumscribe(framework)
        self.wait(0.5)

        # Phase 2: Retrieval
        arrow_f_db.set_color(PRIMARY_COLOR)
        arrow_db_f.set_color(PRIMARY_COLOR)
        
        self.play(Create(arrow_f_db), Write(label_sem), FadeIn(num_2))
        # Removed Circumscribe(db)
        
        self.play(Create(arrow_db_f), Write(label_ctx))
        # Removed Circumscribe(framework)
        self.wait(0.5)

        # Phase 3: Prompt
        arrow_f_llm.set_color(PRIMARY_COLOR)
        self.play(Create(arrow_f_llm), Write(label_prompt), FadeIn(num_3))
        # Removed Circumscribe(llm)
        self.wait(0.5)

        # Phase 4: Response
        arrow_llm_f.set_color(PRIMARY_COLOR)
        arrow_f_c.set_color(PRIMARY_COLOR)
        
        self.play(Create(arrow_llm_f), Write(label_post), FadeIn(num_4))
        # Removed Circumscribe(framework)
        
        self.play(Create(arrow_f_c), Write(label_resp))
        # Removed Circumscribe(client)

        self.wait(3)
#yeha batan endd file

from manim import *
import numpy as np
import random

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             
ICON_BASE_COLOR = "#ec5599"    # Dark Grey
BACKGROUND_COLOR = WHITE       
LIGHT_PINK = "#fbcfe8"         # For Client/User icons
BUTTON_FILL = "#fce7f3"        # Very light pink for text backgrounds

class RAGTargetAudience(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- 1. Component Helpers ---

        def get_user_icon(color=LIGHT_PINK):
            head = Circle(radius=0.3, color=color, fill_color=color, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            body = AnnularSector(
                inner_radius=0, outer_radius=0.5, 
                start_angle=PI, angle=-PI, 
                color=color, fill_opacity=1
            )
            body.stretch(1.2, dim=1)
            body.shift(DOWN * 0.15)
            return VGroup(head, body)

        def get_framework_icon():
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.5)
            spokes = VGroup()
            nodes = VGroup()
            angles = [0, 72, 144, 216, 288]
            radius = 0.65
            for angle in angles:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * radius, np.sin(rad) * radius, 0])
                spokes.add(Line(ORIGIN, pos, color=ICON_BASE_COLOR, stroke_width=2))
                nodes.add(Circle(radius=0.08, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(pos))
            network = VGroup(spokes, hub, nodes)
            box = Square(side_length=1.8, color=ICON_BASE_COLOR, stroke_width=2)
            label = Text("Framework", font_size=16, color=TEXT_COLOR).next_to(box, UP, buff=0.1)
            return VGroup(box, network, label)

        def get_db_icon():
            sq1 = Square(side_length=0.8, color=ICON_BASE_COLOR)
            sq2 = Square(side_length=0.8, color=ICON_BASE_COLOR).shift(UP*0.2 + RIGHT*0.2)
            lines = VGroup(
                Line(sq1.get_corner(UL), sq2.get_corner(UL), color=ICON_BASE_COLOR),
                Line(sq1.get_corner(DR), sq2.get_corner(DR), color=ICON_BASE_COLOR),
                Line(sq1.get_corner(UR), sq2.get_corner(UR), color=ICON_BASE_COLOR),
                Line(sq1.get_corner(DL), sq2.get_corner(DL), color=ICON_BASE_COLOR)
            )
            icon = VGroup(sq2, sq1, lines)
            label = Text("Vector DB", font_size=16, color=TEXT_COLOR).next_to(icon, DOWN, buff=0.1)
            return VGroup(icon, label)

        def get_llm_icon():
            c = Circle(radius=0.5, color=ICON_BASE_COLOR, stroke_width=3)
            t = Text("LLM", font_size=20, color=TEXT_COLOR, weight=BOLD).move_to(c)
            return VGroup(c, t)

        def create_category_block(label_text, icon_color=PRIMARY_COLOR):
            # 1. The Icon
            icon = get_user_icon(color=icon_color).scale(0.4)
            
            # 2. The Text Box (Button style)
            text_obj = Text(label_text, font_size=20, color=TEXT_COLOR, weight=BOLD)
            
            # Create a rectangle behind the text
            rect_width = text_obj.width + 0.6
            rect = RoundedRectangle(
                corner_radius=0.2, 
                height=0.8, 
                width=rect_width, 
                color=ICON_BASE_COLOR, 
                stroke_width=1.5,
                fill_color=BUTTON_FILL,
                fill_opacity=1
            )
            
            text_obj.move_to(rect)
            text_group = VGroup(rect, text_obj)
            
            # Layout: Icon on top, Text box below
            group = VGroup(icon, text_group)
            icon.next_to(text_group, UP, buff=0.25)
            
            return group

        # --- 2. Build Scene Layouts ---

        # A. Crowd Layout
        crowd = VGroup()
        connections = VGroup()
        icons_list = []
        
        # Create scattered icons - Reduced count and increased X range for less congestion
        crowd_size = 30
        for _ in range(crowd_size):
            icon = get_user_icon(color=ICON_BASE_COLOR)
            x_pos = random.uniform(-7.0, 7.0) # Wider range
            y_pos = random.uniform(-1.0, 3.5) 
            icon.move_to([x_pos, y_pos, 0])
            icon.scale(0.4).set_opacity(0.3)
            crowd.add(icon)
            icons_list.append([x_pos, y_pos, 0])

        # Create connections (Network effect)
        for i, pos1 in enumerate(icons_list):
            for j, pos2 in enumerate(icons_list):
                if i < j: 
                    dist = np.linalg.norm(np.array(pos1) - np.array(pos2))
                    if dist < 2.0: 
                        line = Line(pos1, pos2, stroke_width=1, color=ICON_BASE_COLOR, stroke_opacity=0.2)
                        connections.add(line)

        # The "Hero" User - START state
        focus_user = get_user_icon(color=LIGHT_PINK).scale(0.6).move_to(UP * 1.5)
        
        # B. RAG Layout 
        rag_framework = get_framework_icon()
        
        # The "Hero" User - RAG state (Inside the box)
        rag_client = get_user_icon().scale(0.6).next_to(rag_framework, LEFT, buff=1.6)
        
        rag_llm = get_llm_icon().next_to(rag_framework, RIGHT, buff=1.5)
        rag_db = get_db_icon().next_to(rag_framework, DOWN, buff=1.0)
        
        # Changed all to DoubleArrow
        arrows = VGroup(
            DoubleArrow(rag_client.get_right(), rag_framework.get_left(), color=ICON_BASE_COLOR, buff=0.1, stroke_width=2, tip_length=0.15),
            DoubleArrow(rag_framework.get_right(), rag_llm.get_left(), color=ICON_BASE_COLOR, buff=0.1, stroke_width=2, tip_length=0.15),
            DoubleArrow(rag_framework.get_bottom(), rag_db.get_top(), color=ICON_BASE_COLOR, buff=0.1, stroke_width=2, tip_length=0.15)
        )

        rag_group = VGroup(rag_client, rag_framework, rag_llm, rag_db, arrows)
        rag_group.move_to(ORIGIN)

        # The Box surrounding RAG - Increased buff for more space
        rag_box = SurroundingRectangle(rag_group, color=TEXT_COLOR, buff=0.6, stroke_width=4, corner_radius=0.2)
        rag_label = Text("RAG Architecture", font_size=20, color=TEXT_COLOR).next_to(rag_box, UP, buff=0.1)
        rag_full_assembly = VGroup(rag_group, rag_box, rag_label)

        # C. Three Categories Layout
        cat_seekers = create_category_block("Job Seekers")
        cat_pros = create_category_block("Working Professionals")
        cat_leaders = create_category_block("Organization Leaders")

        categories = VGroup(cat_seekers, cat_pros, cat_leaders).arrange(RIGHT, buff=0.6) 
        categories.move_to(DOWN * 2.0)

        # --- 3. Animation Sequence ---

        # INTRO: Crowd and Text
        intro_text = Text("Successful AI Solutions Today", font_size=36, color=TEXT_COLOR).to_edge(DOWN, buff=1.0)
        
        self.play(
            FadeIn(crowd, lag_ratio=0.1), 
            FadeIn(connections, lag_ratio=0.1),
            Write(intro_text), 
            run_time=2
        )
        self.play(FadeIn(focus_user, scale=0.5)) 
        self.wait(0.5)

        # FOCUS: Highlight User
        # Removed .scale() - just color change
        self.play(
            focus_user.animate.set_color(PRIMARY_COLOR),
            crowd.animate.set_opacity(0.1),
            connections.animate.set_opacity(0.05),
            run_time=1
        )
        
        # MORPH: User becomes part of RAG
        self.play(
            FadeOut(crowd),
            FadeOut(connections),
            FadeOut(intro_text),
            ReplacementTransform(focus_user, rag_client),
            run_time=1
        )

        # REVEAL: Show RAG System
        self.play(
            FadeIn(rag_framework),
            FadeIn(rag_llm),
            FadeIn(rag_db),
            Create(arrows),
            run_time=1.5
        )
        
        # EMPHASIS: The Box
        self.play(
            Create(rag_box),
            Write(rag_label),
            run_time=1
        )
        self.wait(1)

        # TRANSITION: Zoom Out & Split
        self.play(
            rag_full_assembly.animate.scale(0.6).to_edge(UP, buff=0.5),
            run_time=1.5
        )

        # Logic: Spawn 3 user icons from the RAG client position
        start_point = rag_client.get_center()
        
        # 1. Icons
        icon_seekers = cat_seekers[0] 
        icon_pros = cat_pros[0]
        icon_leaders = cat_leaders[0]
        
        # 2. Text Boxes
        box_seekers = cat_seekers[1]
        box_pros = cat_pros[1]
        box_leaders = cat_leaders[1]

        # Set initial state for icons (at start point, invisible)
        icon_seekers.move_to(start_point).set_opacity(0)
        icon_pros.move_to(start_point).set_opacity(0)
        icon_leaders.move_to(start_point).set_opacity(0)

        # Animate the split (Icons move to their places)
        self.play(
            LaggedStart(
                icon_seekers.animate.set_opacity(1).move_to(cat_seekers[0].get_center()),
                icon_pros.animate.set_opacity(1).move_to(cat_pros[0].get_center()),
                icon_leaders.animate.set_opacity(1).move_to(cat_leaders[0].get_center()),
                lag_ratio=0.1
            ),
            run_time=1.5
        )

        # Reveal the text boxes (Fade in only)
        self.play(
            FadeIn(box_seekers, shift=UP*0.2),
            FadeIn(box_pros, shift=UP*0.2),
            FadeIn(box_leaders, shift=UP*0.2),
            run_time=1
        )

        self.wait(3)

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             
ICON_BASE_COLOR = "#ec5599"    # Lighter Grey (was #4b5563)
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
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.0) # Reduced width
            spokes = VGroup()
            nodes = VGroup()
            angles = [0, 72, 144, 216, 288] 
            radius = 0.65
            for angle in angles:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * radius, np.sin(rad) * radius, 0])
                spokes.add(Line(start=ORIGIN, end=pos, color=ICON_BASE_COLOR, stroke_width=1.5)) # Reduced width
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
            circle = Circle(radius=0.6, color=ICON_BASE_COLOR, stroke_width=2.5) # Reduced width
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
            line = Line(start=start, end=end, color=color, stroke_width=2.0) # Reduced width
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

        # Arrows
        arrow_c_f = create_straight_arrow(client[0].get_right() + RIGHT*0.1, framework[0].get_left() + LEFT*0.1)
        arrow_f_c = create_straight_arrow(framework[0].get_left() + LEFT*0.1 + UP*0.4, client[0].get_right() + RIGHT*0.1 + UP*0.4)
        arrow_f_llm = create_straight_arrow(framework[0].get_right() + RIGHT*0.1, llm[0].get_left() + LEFT*0.1)
        arrow_llm_f = create_straight_arrow(llm[0].get_left() + LEFT*0.1 + UP*0.4, framework[0].get_right() + RIGHT*0.1 + UP*0.4)
        arrow_f_db = create_straight_arrow(framework[0].get_bottom() + LEFT*0.4 + DOWN*0.1, db[0].get_top() + LEFT*0.4 + UP*0.1)
        arrow_db_f = create_straight_arrow(db[0].get_top() + RIGHT*0.4 + UP*0.1, framework[0].get_bottom() + RIGHT*0.4 + DOWN*0.1)
        arrow_content_db = create_straight_arrow(content[0].get_left() + LEFT*0.1, db[0].get_right() + RIGHT*0.1)

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
            llm_img = ImageMobject(r"D:\manim\images\llm.jpg").set_height(2.5)
        except:
            rect = Rectangle(color=RED, fill_opacity=0.5, height=2.5, width=4)
            t = Text("LLM.jpg", color=WHITE, font_size=24).move_to(rect)
            llm_img = Group(rect, t)
        
        llm_img.next_to(llm, RIGHT, buff=0.5)
        focus_group_1 = Group(llm, llm_img)

        self.play(
            all_elements.animate.set_opacity(0.15), # Fade others
            llm.animate.set_opacity(1), # Keep target visible, but NO style change
            self.camera.frame.animate.move_to(focus_group_1.get_center()).set(width=focus_group_1.width * 1.4),
            run_time=2
        )
        self.play(FadeIn(llm_img))
        self.wait(3)
        
        self.play(FadeOut(llm_img), run_time=0.5)
        self.play(
            Restore(self.camera.frame), 
            all_elements.animate.set_opacity(1), 
            run_time=1.5
        )

        # --- ZOOM 2: Semantic Search ---
        try:
            sem_img = ImageMobject(r"D:\manim\images\semantic.jpg").set_height(2.5)
        except:
            rect = Rectangle(color=GREEN, fill_opacity=0.5, height=2.5, width=4)
            t = Text("semantic.jpg", color=WHITE, font_size=24).move_to(rect)
            sem_img = Group(rect, t)

        sem_img.next_to(label_sem, LEFT, buff=0.5)
        focus_group_2 = Group(label_sem, sem_img)

        self.play(
            all_elements.animate.set_opacity(0.15),
            label_sem.animate.set_opacity(1),
            self.camera.frame.animate.move_to(focus_group_2.get_center()).set(width=focus_group_2.width * 1.4),
            run_time=2
        )
        self.play(FadeIn(sem_img))
        self.wait(3)

        self.play(FadeOut(sem_img), run_time=0.5)
        self.play(
            Restore(self.camera.frame), 
            all_elements.animate.set_opacity(1), 
            run_time=1.5
        )

        # --- ZOOM 3: Fine Tuning ---
        try:
            ft_img = ImageMobject(r"D:\manim\images\finetuning.jpg").set_height(2.5)
        except:
            rect = Rectangle(color=BLUE, fill_opacity=0.5, height=2.5, width=4)
            t = Text("finetuning.jpg", color=WHITE, font_size=24).move_to(rect)
            ft_img = Group(rect, t)

        ft_img.next_to(fine_tuning, UR, buff=0.5)
        focus_group_3 = Group(fine_tuning, ft_img)

        self.play(
            all_elements.animate.set_opacity(0.15),
            fine_tuning.animate.set_opacity(1),
            self.camera.frame.animate.move_to(focus_group_3.get_center()).set(width=focus_group_3.width * 1.4),
            run_time=2
        )
        self.play(FadeIn(ft_img))
        self.wait(3)

        self.play(FadeOut(ft_img), run_time=0.5)
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

        # Arrows
        arrow_c_f = create_straight_arrow(client[0].get_right() + RIGHT*0.1, framework[0].get_left() + LEFT*0.1)
        arrow_f_c = create_straight_arrow(framework[0].get_left() + LEFT*0.1 + UP*0.4, client[0].get_right() + RIGHT*0.1 + UP*0.4)
        arrow_f_llm = create_straight_arrow(framework[0].get_right() + RIGHT*0.1, llm[0].get_left() + LEFT*0.1)
        arrow_llm_f = create_straight_arrow(llm[0].get_left() + LEFT*0.1 + UP*0.4, framework[0].get_right() + RIGHT*0.1 + UP*0.4)
        arrow_f_db = create_straight_arrow(framework[0].get_bottom() + LEFT*0.4 + DOWN*0.1, db[0].get_top() + LEFT*0.4 + UP*0.1)
        arrow_db_f = create_straight_arrow(db[0].get_top() + RIGHT*0.4 + UP*0.1, framework[0].get_bottom() + RIGHT*0.4 + DOWN*0.1)
        arrow_content_db = create_straight_arrow(content[0].get_left() + LEFT*0.1, db[0].get_right() + RIGHT*0.1)

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

        # Arrows
        arrow_c_f = create_straight_arrow(client[0].get_right(), framework[0].get_left(), color=PRIMARY_COLOR)
        arrow_f_c = create_straight_arrow(framework[0].get_left(), client[0].get_right(), color=PRIMARY_COLOR)
        arrow_f_llm = create_straight_arrow(framework[0].get_right(), llm[0].get_left(), color=PRIMARY_COLOR)
        arrow_llm_f = create_straight_arrow(llm[0].get_left(), framework[0].get_right(), color=PRIMARY_COLOR)
        arrow_f_db = create_straight_arrow(framework[0].get_bottom(), db[0].get_top(), color=PRIMARY_COLOR)
        arrow_db_f = create_straight_arrow(db[0].get_top(), framework[0].get_bottom(), color=PRIMARY_COLOR)
        arrow_content_db = create_straight_arrow(content[0].get_left(), db[0].get_right(), color=ICON_BASE_COLOR)

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

        arrow_c_f = create_straight_arrow(client[0].get_right() + RIGHT*0.1, framework[0].get_left() + LEFT*0.1, color=PRIMARY_COLOR)
        arrow_f_db = create_straight_arrow(framework[0].get_bottom() + LEFT*0.4 + DOWN*0.1, db[0].get_top() + LEFT*0.4 + UP*0.1, color=PRIMARY_COLOR)
        arrow_db_f = create_straight_arrow(db[0].get_top() + RIGHT*0.4 + UP*0.1, framework[0].get_bottom() + RIGHT*0.4 + DOWN*0.1, color=PRIMARY_COLOR)
        arrow_content_db = create_straight_arrow(content[0].get_left() + LEFT*0.1, db[0].get_right() + RIGHT*0.1, color=ICON_BASE_COLOR)

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

        # 5. Setup Cards Data
        card_data = [
            ("Company Expense Policy", "PDF", "Home office equipment\nup to $1,000 requires\nmanager approval."),
            ("HR Addendum", "Word Doc", "Remote employees may\nexpense additional\nequipment once per year."),
            ("Email from Finance", "Text", "Monitor reimbursements\nabove $800 are\ntemporarily paused."),
            ("Employee Profile", "Data", "Role: Software Engineer\nRemote Status: Yes")
        ]

        # Prepare list to hold the Card Backgrounds and Card Texts separately
        card_bgs = VGroup()
        card_contents = VGroup() # Holds title, type, lines, body

        for i, (title_text, type_text, body_text) in enumerate(card_data):
            # Taller, narrower card
            card_bg = RoundedRectangle(corner_radius=0.15, height=4.5, width=3.2, color=PRIMARY_COLOR, stroke_width=2.5, fill_color=WHITE, fill_opacity=1)
            
            t_obj = Text(title_text, font_size=16, color=PRIMARY_COLOR, weight=BOLD).move_to(card_bg.get_top() + DOWN*0.5)
            if t_obj.width > 2.8:
                t_obj.scale_to_fit_width(2.8)
            
            type_obj = Text(f"({type_text})", font_size=14, color=ICON_BASE_COLOR, slant=ITALIC).next_to(t_obj, DOWN, buff=0.15)
            
            line = Line(card_bg.get_left() + RIGHT*0.2, card_bg.get_right() + LEFT*0.2, color=ICON_BASE_COLOR, stroke_width=1).next_to(type_obj, DOWN, buff=0.2)
            
            lines = body_text.split('\n')
            b_obj = VGroup(*[Text(l, font_size=16, color=TEXT_COLOR) for l in lines]).arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.1)
            b_obj.next_to(line, DOWN, buff=0.2).align_to(line, LEFT)
            
            if b_obj.width > 2.8:
                b_obj.scale_to_fit_width(2.8)
            b_obj.move_to(card_bg.get_center() + DOWN*0.5)
            
            card_bgs.add(card_bg)
            card_contents.add(VGroup(t_obj, type_obj, line, b_obj))

        # Arrange backgrounds first to get positions
        card_bgs.arrange(RIGHT, buff=0.25)
        card_bgs.next_to(top_group, DOWN, buff=0.5)
        if card_bgs.width > 13.5:
             card_bgs.scale_to_fit_width(13.5)

        # Move contents to match their backgrounds' final positions
        for bg, content in zip(card_bgs, card_contents):
            t, ty, l, b = content
            t.move_to(bg.get_top() + DOWN*0.5)
            ty.next_to(t, DOWN, buff=0.15)
            l.put_start_and_end_on(bg.get_left() + RIGHT*0.2, bg.get_right() + LEFT*0.2)
            l.next_to(ty, DOWN, buff=0.2)
            b.next_to(l, DOWN, buff=0.2).align_to(l, LEFT)
            b.move_to(bg.get_center() + DOWN*0.5)


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
        
        # Vector DB is completely removed!
        
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        ft_connector = DashedLine(start=fine_tuning.get_bottom(), end=llm.get_top(), color=ICON_BASE_COLOR, stroke_width=2)

        arrow_c_f = create_straight_arrow(client[0].get_right() + RIGHT*0.1, framework[0].get_left() + LEFT*0.1, color=PRIMARY_COLOR)
        arrow_f_c = create_straight_arrow(framework[0].get_left() + LEFT*0.1 + UP*0.4, client[0].get_right() + RIGHT*0.1 + UP*0.4, color=PRIMARY_COLOR)
        arrow_f_llm = create_straight_arrow(framework[0].get_right() + RIGHT*0.1, llm[0].get_left() + LEFT*0.1, color=PRIMARY_COLOR)
        arrow_llm_f = create_straight_arrow(llm[0].get_left() + LEFT*0.1 + UP*0.4, framework[0].get_right() + RIGHT*0.1 + UP*0.4, color=PRIMARY_COLOR)

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
        q_group = VGroup(q_box, q_content) # No position yet
        
        # Create a temporary centered group to calculate positions
        # Client on Left, Question on Right
        temp_top_group = VGroup(client.copy(), q_group.copy()).arrange(RIGHT, buff=0.5)
        temp_top_group.move_to(UP * 2.5) # Center this group at the top
        
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
            # Slightly larger radius to ensure text fits comfortably
            circle = Circle(radius=0.75, color=stroke_color, stroke_width=4, fill_color=WHITE, fill_opacity=1)
            
            # Dynamic font sizing to prevent overflow
            font_s = 20 if len(label_text) > 5 else 24
            text = Text(label_text, font_size=font_s, color=TEXT_COLOR, weight=BOLD, line_spacing=1).move_to(circle)
            
            # Important: Set z_index high so documents pass BEHIND it
            group = VGroup(circle, text)
            group.set_z_index(10) 
            return group

        def get_fine_tuning_icon():
            # Original simple circle, no gears
            circle = Circle(radius=0.45, color=ICON_BASE_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            text = Text("Fine\nTuning", font_size=12, color=TEXT_COLOR, line_spacing=1).move_to(circle)
            
            # Important: Set z_index high so documents pass BEHIND it
            group = VGroup(circle, text)
            group.set_z_index(10)
            return group

        def get_document_icon(color=PRIMARY_COLOR):
            # Simple clean doc icon
            doc = Rectangle(height=0.6, width=0.45, color=color, fill_color=WHITE, fill_opacity=1, stroke_width=2)
            lines = VGroup(*[Line(start=LEFT*0.12, end=RIGHT*0.12, color=color, stroke_width=1.5).shift(UP*0.1 - i*0.1) for i in range(3)])
            lines.move_to(doc.get_center())
            return VGroup(doc, lines)

        def create_arrow(start, end, color=ICON_BASE_COLOR):
            return Line(start=start, end=end, color=color, stroke_width=3).add_tip(tip_length=0.2, tip_width=0.2)

        # --- PART 1: The Initial Scene (RAG Model) ---
        
        # Instantiate Objects
        title = Text("RAG Architecture Model", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)
        
        framework = get_framework_icon().shift(UP*0.5) 
        client = get_client_icon().next_to(framework, LEFT, buff=2.0).shift(DOWN*0.2)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.0).shift(DOWN*0.2)
        
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        ft_connector = DashedLine(start=fine_tuning.get_bottom(), end=llm.get_top(), color=ICON_BASE_COLOR, stroke_width=2)

        # Arrows & Labels
        arrow_c_f = create_arrow(client[0].get_right() + RIGHT*0.1, framework[0].get_left() + LEFT*0.1, color=PRIMARY_COLOR)
        arrow_f_c = create_arrow(framework[0].get_left() + LEFT*0.1 + UP*0.4, client[0].get_right() + RIGHT*0.1 + UP*0.4, color=PRIMARY_COLOR)
        arrow_f_llm = create_arrow(framework[0].get_right() + RIGHT*0.1, llm[0].get_left() + LEFT*0.1, color=PRIMARY_COLOR)
        arrow_llm_f = create_arrow(llm[0].get_left() + LEFT*0.1 + UP*0.4, framework[0].get_right() + RIGHT*0.1 + UP*0.4, color=PRIMARY_COLOR)

        label_q = Text("Question", font_size=16, color=TEXT_COLOR).next_to(arrow_c_f, DOWN, buff=0.1)
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR).next_to(arrow_f_c, UP, buff=0.1)
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR).next_to(arrow_f_llm, DOWN, buff=0.1)
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).next_to(arrow_llm_f, UP, buff=0.1)
        
        # Draw Initial State
        self.add(title, client, framework, llm, fine_tuning, ft_connector, arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f, label_q, label_resp, label_prompt, label_post)
        self.wait(1.5)

        # --- PART 2: The Transition (Fade to Focus) ---
        
        # Fade out everything EXCEPT Client, Fine Tuning, and LLM
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
        
        base_model_label = Text("Open Source Model (e.g. Llama)", font_size=16, color=OUTDATED_COLOR).next_to(llm, DOWN)
        self.play(FadeIn(base_model_label))
        self.wait(1)

        # --- PART 3: The "Temptation" (Organization Data) ---
        
        # Create Org Data (Documents)
        # Note: z_index=0 by default, so they will be below Fine Tuning (z=10)
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
        self.remove(moving_docs) # "Absorbed"
        
        # Animation: Processed info moves to LLM
        processed_stream = Line(start=fine_tuning.get_right(), end=llm.get_left(), color=PRIMARY_COLOR, stroke_width=5)
        
        # Ensure the stream is also behind the circles
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
        
        # 3. The Retraining Process (Progress Bar)
        progress_bar_bg = Rectangle(width=3, height=0.2, color=OUTDATED_COLOR, fill_opacity=0, stroke_width=1).next_to(fine_tuning, DOWN, buff=0.5)
        
        # FIX: stroke_width=0 prevents the "vertical line" glitch when width is near 0
        progress_bar_fill = Rectangle(width=0, height=0.2, color=ACCENT_COLOR, fill_opacity=1, stroke_width=0).align_to(progress_bar_bg, LEFT)
        
        cost_text = Text("Retraining Cost: $$$", font_size=16, color=ACCENT_COLOR).next_to(progress_bar_bg, DOWN, buff=0.1)
        
        self.play(
            FadeIn(progress_bar_bg),
            Write(cost_text)
        )
        
        # Move new blue data to fine tuning
        moving_new_docs = org_data.copy()
        
        # Slow fill animation
        self.play(
            moving_new_docs.animate.move_to(fine_tuning.get_center()),
            progress_bar_fill.animate.set_width(3), 
            run_time=2.5,
            rate_func=linear
        )
        self.remove(moving_new_docs)
        
        # Result: Model becomes Blue (Updated)
        updated_llm = get_llm_icon("Custom\nModel", stroke_color=DATA_COLOR)
        updated_llm.move_to(outdated_llm.get_center())
        
        self.play(
            ReplacementTransform(outdated_llm, updated_llm),
            FadeOut(warning)
        )
        
        # Final Text
        inefficient_label = Text("Impractical for frequent updates", font_size=24, color=ACCENT_COLOR).move_to(UP * 2.5)
        
        bg_rect = SurroundingRectangle(
            inefficient_label, 
            color=WHITE, 
            fill_color=WHITE, 
            fill_opacity=0.85,
            buff=0.15
        )
        bg_rect.set_stroke(width=0)
        
        self.play(
            FadeIn(bg_rect),
            Write(inefficient_label)
        )
        
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

        def create_arrow(start, end, color=ICON_BASE_COLOR):
            return Line(start=start, end=end, color=color, stroke_width=3).add_tip(tip_length=0.2, tip_width=0.2)

        # =========================================
        # PHASE 1: The Initial Full Diagram (RAG)
        # =========================================
        
        # Instantiate Objects
        title = Text("Standard RAG Architecture", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)
        
        framework = get_framework_icon()
        client = get_client_icon().next_to(framework, LEFT, buff=2.5)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.5)
        
        # Arrows 
        # Left Side (Client <-> Framework)
        arrow_c_f = create_arrow(client[0].get_right() + RIGHT*0.1, framework[0].get_left() + LEFT*0.1, color=PRIMARY_COLOR)
        arrow_f_c = create_arrow(framework[0].get_left() + LEFT*0.1 + UP*0.4, client[0].get_right() + RIGHT*0.1 + UP*0.4, color=PRIMARY_COLOR)
        
        # Right Side (Framework <-> LLM)
        arrow_f_llm = create_arrow(framework[0].get_right() + RIGHT*0.1, llm[0].get_left() + LEFT*0.1, color=PRIMARY_COLOR)
        arrow_llm_f = create_arrow(llm[0].get_left() + LEFT*0.1 + UP*0.4, framework[0].get_right() + RIGHT*0.1 + UP*0.4, color=PRIMARY_COLOR)

        # Labels
        label_q = Text("Question", font_size=16, color=TEXT_COLOR).next_to(arrow_c_f, DOWN, buff=0.1)
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR).next_to(arrow_f_c, UP, buff=0.1)
        
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR, line_spacing=1).next_to(arrow_f_llm, DOWN, buff=0.1)
        
        # --- NEW LABEL HERE ---
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).next_to(arrow_llm_f, UP, buff=0.1)

        
        # Draw Initial State
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

        # 1. Define what to fade out (everything EXCEPT client and llm)
        # Note: We must include the new label_post in the fade group
        elements_to_fade = VGroup(
            title, framework,
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f,
            label_q, label_resp, label_prompt, label_post
        )

        # 2. Fade out unnecessary elements
        self.play(
            FadeOut(elements_to_fade),
            run_time=1.5
        )

        # 3. Reposition Client and LLM to center stage
        target_client_pos = LEFT * 3.5
        target_llm_pos = RIGHT * 3.5

        self.play(
            client.animate.move_to(target_client_pos),
            llm.animate.move_to(target_llm_pos),
            run_time=1.5
        )
        self.wait(0.5)

        # 4. Introduce "Hallucination" text with emphasis
        hallucination_text = Text("Hallucination", font_size=36, color=ACCENT_COLOR, weight=BOLD)
        hallucination_text.move_to(ORIGIN)

        # Write text and add a slight "pop" effect
        self.play(Write(hallucination_text))
        self.play(
            hallucination_text.animate.scale(1.2),
            run_time=0.4,
            rate_func=there_and_back # Scales up then immediately back down
        )

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
            
            # CHANGED: Added t2c (text-to-color) to make the specific phrase BLUE
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

        # Arrows
        c_right = client[0].get_right()
        f_left = framework[0].get_left()
        
        arrow_c_f = create_straight_arrow(
            np.array([c_right[0] + 0.1, c_right[1] - 0.2, 0]), 
            np.array([f_left[0] - 0.1, f_left[1] - 0.2, 0])
        )
        
        arrow_f_c = create_straight_arrow(
            np.array([f_left[0] - 0.1, f_left[1] + 0.5, 0]), 
            np.array([c_right[0] + 0.1, c_right[1] + 0.5, 0])
        )
        
        f_right = framework[0].get_right()
        l_left = llm[0].get_left()
        
        arrow_f_llm = create_straight_arrow(f_right + RIGHT*0.1 + DOWN*0.2, l_left + LEFT*0.1 + DOWN*0.2)
        arrow_llm_f = create_straight_arrow(l_left + LEFT*0.1 + UP*0.6, f_right + RIGHT*0.1 + UP*0.6)
        
        f_bottom = framework[0].get_bottom()
        d_top = db[0].get_top()
        
        arrow_f_db = create_straight_arrow(f_bottom + LEFT*0.5 + DOWN*0.1, d_top + LEFT*0.5 + UP*0.1)
        arrow_db_f = create_straight_arrow(d_top + RIGHT*0.5 + UP*0.1, f_bottom + RIGHT*0.5 + DOWN*0.1)
        
        arrow_content_db = create_straight_arrow(content[0].get_left() + LEFT*0.1, db[0].get_right() + RIGHT*0.1)

        # Labels
        label_q = Text("Question", font_size=16, color=TEXT_COLOR, slant=ITALIC)
        label_q.move_to(arrow_c_f.get_center()).shift(DOWN * 0.25)
        
        num_1 = get_number_circle(1).next_to(label_q, LEFT, buff=0.1)
        
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR, slant=ITALIC)
        label_resp.move_to(arrow_f_c.get_center()).shift(UP * 0.25)
        
        label_sem = Text("Semantic\nSearch", font_size=14, color=TEXT_COLOR, line_spacing=1)
        label_sem.move_to(arrow_f_db.get_center()).shift(LEFT * 0.6) 
        
        num_2 = get_number_circle(2).next_to(label_sem, DOWN, buff=0.1)
        
        # NOTE: Label is already BLUE_COLOR from previous instruction, confirming it here.
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
        
        # CHANGED: Arrow color to BLUE_COLOR
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

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
SECONDARY_COLOR = "#fce7f3"    # Very Light Pink
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
BLUE_COLOR = "#3b82f6"         # Blue for context/reasoning
BACKGROUND_COLOR = WHITE       # White background

class RAGProfessionalSceneCentered(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- 1. Introduction Text ---
        intro_text_1 = Text("Most companies skip expensive Fine-Tuning...", font_size=32, color=TEXT_COLOR)
        intro_text_2 = Text("...and deploy RAG solutions instead.", font_size=32, color=PRIMARY_COLOR, weight=BOLD)
        
        intro_group = VGroup(intro_text_1, intro_text_2).arrange(DOWN, buff=0.3)
        
        self.play(Write(intro_group), run_time=2)
        self.wait(1.5)
        self.play(FadeOut(intro_group, shift=UP))

        # --- 2. Acronym Setup ---
        # Large, bold letters centered initially
        r_char = Text("R", font_size=120, color=PRIMARY_COLOR, weight=BOLD)
        a_char = Text("A", font_size=120, color=PRIMARY_COLOR, weight=BOLD)
        g_char = Text("G", font_size=120, color=PRIMARY_COLOR, weight=BOLD)

        acronym_group = VGroup(r_char, a_char, g_char).arrange(RIGHT, buff=2.0)
        acronym_group.move_to(ORIGIN)

        self.play(LaggedStart(
            FadeIn(r_char, shift=DOWN), 
            FadeIn(a_char, shift=DOWN), 
            FadeIn(g_char, shift=DOWN), 
            lag_ratio=0.2
        ))
        self.wait(1)

        # --- 3. Step 1: Retrieval (Focus on R - Left Side Layout) ---
        
        # Focus R: Scale up R to LEFT edge, fade/shrink A and G and move them away
        self.play(
            r_char.animate.scale(1.2).to_edge(LEFT, buff=1.0).shift(UP*0.5),
            a_char.animate.scale(0.6).set_color(GRAY).move_to(UP * 2.5 + RIGHT * 1.5), # Move out of way
            g_char.animate.scale(0.6).set_color(GRAY).move_to(UP * 2.5 + RIGHT * 3.0),
        )

        # Title next to R
        r_title = Text("Retrieval", font_size=48, color=TEXT_COLOR, weight=BOLD).next_to(r_char, RIGHT, buff=0.5).align_to(r_char, UP).shift(DOWN*0.2)
        
        # Content aligned left
        r_content = VGroup(
            Text("• Semantic Search", font_size=32, color=TEXT_COLOR),
            Text("• Based on meaning, not just keywords", font_size=28, color=BLUE_COLOR, slant=ITALIC)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(r_title, DOWN, buff=0.4).align_to(r_title, LEFT)

        # Visual Abstract (Query -> Doc) aligned left
        query_box = RoundedRectangle(corner_radius=0.1, height=0.5, width=2, color=PRIMARY_COLOR)
        query_lbl = Text("Query", font_size=20, color=PRIMARY_COLOR).move_to(query_box)
        query_grp = VGroup(query_box, query_lbl).next_to(r_content, DOWN, buff=0.8).align_to(r_content, LEFT)

        arrow = Arrow(start=LEFT, end=RIGHT, color=TEXT_COLOR).next_to(query_grp, RIGHT, buff=0.2)
        
        doc_box = Rectangle(height=0.6, width=0.5, color=BLUE_COLOR, fill_opacity=0.2, fill_color=BLUE_COLOR)
        doc_lbl = Text("Doc", font_size=16, color=BLUE_COLOR).move_to(doc_box)
        doc_grp = VGroup(doc_box, doc_lbl).next_to(arrow, RIGHT, buff=0.2)

        self.play(Write(r_title))
        self.play(FadeIn(r_content, shift=RIGHT))
        self.play(GrowFromCenter(query_grp))
        self.play(Create(arrow), FadeIn(doc_grp, shift=LEFT))
        self.wait(3)

        # Cleanup R - Move R to top left dim position
        self.play(
            FadeOut(r_title), FadeOut(r_content), FadeOut(query_grp), FadeOut(arrow), FadeOut(doc_grp),
            r_char.animate.scale(1/1.2 * 0.6).set_color(GRAY).move_to(UP * 2.5 + LEFT * 3.0), 
        )

        # --- 4. Step 2: Augmented (Focus on A - Center Layout) ---

        # Focus A: Bring A to CENTER TOP focus
        self.play(
            a_char.animate.scale(1/0.6 * 1.2).set_color(PRIMARY_COLOR).move_to(UP * 2.5),
            # G stays dim where it is
        )

        # Title below A (Centered)
        a_title = Text("Augmented", font_size=48, color=TEXT_COLOR, weight=BOLD).next_to(a_char, DOWN, buff=0.5)
        
        # Content below Title (Centered)
        a_content = VGroup(
            Text("LLM reads retrieved info (Context)", font_size=32, color=TEXT_COLOR),
            Text("Applies reasoning to data", font_size=28, color=BLUE_COLOR, slant=ITALIC)
        ).arrange(DOWN, buff=0.2).next_to(a_title, DOWN, buff=0.5)

        # Visual Abstract: [Doc] + [Logic] (Centered)
        vis_doc = doc_grp.copy() # Reuse doc look
        plus = Text("+", font_size=36, color=TEXT_COLOR)
        vis_logic = Text("Reasoning", font_size=24, color=PRIMARY_COLOR, weight=BOLD)
        
        # Group elements horizontally then center beneath content
        vis_group = VGroup(vis_doc, plus, vis_logic).arrange(RIGHT, buff=0.3).next_to(a_content, DOWN, buff=0.8)
        
        vis_bracket = Brace(vis_group, DOWN, color=TEXT_COLOR)
        vis_context = Text("Context", font_size=20, color=TEXT_COLOR).next_to(vis_bracket, DOWN, buff=0.1)

        self.play(Write(a_title))
        self.play(FadeIn(a_content, shift=UP))
        self.play(FadeIn(vis_doc), Write(plus), Write(vis_logic))
        self.play(GrowFromCenter(vis_bracket), FadeIn(vis_context))
        self.wait(3)

        # Cleanup A - Move A to top left dim position next to R
        self.play(
            FadeOut(a_title), FadeOut(a_content), FadeOut(vis_doc), FadeOut(plus), FadeOut(vis_logic), FadeOut(vis_bracket), FadeOut(vis_context),
            a_char.animate.scale(1/1.2 * 0.6).set_color(GRAY).move_to(UP * 2.5 + LEFT * 1.5),
        )

        # --- 5. Step 3: Generation (Focus on G - Center Layout) ---

        # Focus G: Bring G to CENTER TOP focus
        self.play(
            g_char.animate.scale(1/0.6 * 1.2).set_color(PRIMARY_COLOR).move_to(UP * 2.5),
        )

        # Title below G (Centered)
        g_title = Text("Generation", font_size=48, color=TEXT_COLOR, weight=BOLD).next_to(g_char, DOWN, buff=0.5)
        
        # Content below Title (Centered)
        g_content = VGroup(
            Text("Generates new response", font_size=32, color=TEXT_COLOR),
            Text("Uses Context + Internet/Knowledge", font_size=28, color=BLUE_COLOR, slant=ITALIC)
        ).arrange(DOWN, buff=0.2).next_to(g_title, DOWN, buff=0.5)

        # REMOVED: Typing lines animation

        self.play(Write(g_title))
        self.play(FadeIn(g_content, shift=UP))
        self.wait(3)

        # --- 6. Conclusion ---

        # Reset all letters to center positions from their current locations
        self.play(
            FadeOut(g_title), FadeOut(g_content),
            r_char.animate.scale(1/0.6).set_color(PRIMARY_COLOR).move_to(ORIGIN + LEFT * 2.5),
            a_char.animate.scale(1/0.6).set_color(PRIMARY_COLOR).move_to(ORIGIN),
            g_char.animate.scale(1/1.2).move_to(ORIGIN + RIGHT * 2.5),
        )

        # Reveal full acronym words below
        full_r = Text("Retrieval", font_size=24, color=TEXT_COLOR).next_to(r_char, DOWN, buff=0.3)
        full_a = Text("Augmented", font_size=24, color=TEXT_COLOR).next_to(a_char, DOWN, buff=0.3)
        full_g = Text("Generation", font_size=24, color=TEXT_COLOR).next_to(g_char, DOWN, buff=0.3)

        self.play(LaggedStart(Write(full_r), Write(full_a), Write(full_g), lag_ratio=0.2))
        
        self.wait(3)