from manim import *
import numpy as np
import random

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # Black text
ICON_BASE_COLOR = "#ec5599"    # Primary Pink for icons
BACKGROUND_COLOR = WHITE       # White background
LIGHT_PINK = "#fbcfe8"         # Solid Light Pink
GRID_COLOR = "#6C6E72"         # Light grey
CHUNK_RED = "#db2777"          # Primary Pink
CHUNK_BLUE = "#0ea5e9"         # Contrast Blue

class RAGArchitectureSceneFinalFix(ThreeDScene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Helpers ---
        def get_client_icon():
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0).shift(UP * 0.5)
            body = AnnularSector(inner_radius=0, outer_radius=0.5, start_angle=PI, angle=-PI, color=LIGHT_PINK, fill_opacity=1)
            body.stretch(1.2, dim=1).shift(DOWN * 0.15)
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            hub = Circle(radius=0.25, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2.5)
            spokes, nodes = VGroup(), VGroup()
            for angle in [0, 72, 144, 216, 288]:
                rad = angle * DEGREES
                pos = np.array([np.cos(rad) * 0.65, np.sin(rad) * 0.65, 0])
                spokes.add(Line(start=ORIGIN, end=pos, color=ICON_BASE_COLOR, stroke_width=2))
                nodes.add(Circle(radius=0.08, color=ICON_BASE_COLOR, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(pos))
            box = Square(side_length=1.8, color=ICON_BASE_COLOR, stroke_width=2)
            icon_group = VGroup(box, VGroup(spokes, hub, nodes))
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(icon_group, UP, buff=0.1)
            return VGroup(icon_group, label)

        def get_db_icon():
            front = Square(side_length=0.9, color=ICON_BASE_COLOR)
            back = Square(side_length=0.9, color=ICON_BASE_COLOR).shift(UP*0.25 + RIGHT*0.25)
            connectors = VGroup(*[Line(front.get_corner(c), back.get_corner(c), color=ICON_BASE_COLOR) for c in [UL, UR, DL, DR]])
            dots = VGroup(
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front.get_center() + LEFT*0.15),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(back.get_center() + RIGHT*0.15 + UP*0.1),
                Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front.get_center() + DOWN*0.15 + RIGHT*0.1),
            )
            icon_group = VGroup(back, front, connectors, dots)
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
                corner = Polygon(doc.get_corner(UR), doc.get_corner(UR)+LEFT*0.12, doc.get_corner(UR)+DOWN*0.12+LEFT*0.12, doc.get_corner(UR)+DOWN*0.12, color=color, stroke_width=1.5, fill_color=BACKGROUND_COLOR, fill_opacity=1)
                return VGroup(doc, corner)
            orig_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(6)]).arrange_in_grid(rows=2, buff=0.08)
            new_docs = VGroup(*[make_doc(PRIMARY_COLOR) for _ in range(4)]).arrange_in_grid(rows=2, buff=0.08)
            all_docs = VGroup(orig_docs, new_docs).arrange(RIGHT, buff=0.3)
            orig_label = Text("Documents", font_size=12, color=PRIMARY_COLOR).next_to(orig_docs, DOWN, buff=0.1)
            new_label = Text("Files", font_size=12, color=PRIMARY_COLOR).next_to(new_docs, DOWN, buff=0.1)
            return VGroup(all_docs, orig_label, new_label)

        def create_straight_arrow(start, end, color=ICON_BASE_COLOR):
            return Line(start=start, end=end, color=color, stroke_width=3).add_tip(tip_length=0.2, tip_width=0.2)

        def get_3d_grid_cube():
            axes = ThreeDAxes(x_range=[-1,1,0.5], y_range=[-1,1,0.5], z_range=[-1,1,0.5], x_length=2.5, y_length=2.5, z_length=2.5, axis_config={"color": GRID_COLOR, "stroke_width": 1.5})
            cube_cage = Cube(side_length=2.5, fill_opacity=0, stroke_color=GRID_COLOR, stroke_width=2)
            pos_dots = VGroup(*[Dot3D(point=[random.uniform(-0.8,0.8) for _ in range(3)], radius=0.08, color=CHUNK_RED) for _ in range(6)])
            neg_dots = VGroup(*[Dot3D(point=[random.uniform(-0.8,0.8) for _ in range(3)], radius=0.08, color=CHUNK_BLUE) for _ in range(4)])
            return VGroup(axes, cube_cage), pos_dots, neg_dots

        # --- 2. Initial Layout (Untouched) ---
        title = Text("RAG Architecture Model", font_size=32, color=TEXT_COLOR).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)
        framework = get_framework_icon().shift(UP*0.5)
        client = get_client_icon().next_to(framework, LEFT, buff=2.0).shift(DOWN*0.2)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.0).shift(DOWN*0.2)
        db = get_db_icon().next_to(framework, DOWN, buff=1.5)
        content = get_content_icons().next_to(db, RIGHT, buff=0.8).align_to(db, DOWN)
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        ft_connector = DashedLine(start=fine_tuning.get_bottom(), end=llm.get_top(), color=ICON_BASE_COLOR, stroke_width=2, dash_length=0.1)

        # Static Arrows for Initial View
        y1 = client[0].get_center()[1]
        a_cf = create_straight_arrow([client[0].get_right()[0]+0.1, y1, 0], [framework[0].get_left()[0]-0.1, y1, 0])
        a_fc = create_straight_arrow([framework[0].get_left()[0]-0.1, y1+0.4, 0], [client[0].get_right()[0]+0.1, y1+0.4, 0])
        y3 = framework[0].get_center()[1]
        a_fl = create_straight_arrow([framework[0].get_right()[0]+0.1, y3, 0], [llm[0].get_left()[0]-0.1, y3, 0])
        a_lf = create_straight_arrow([llm[0].get_left()[0]-0.1, y3+0.4, 0], [framework[0].get_right()[0]+0.1, y3+0.4, 0])
        x1 = framework[0].get_center()[0] - 0.4
        a_fd = create_straight_arrow([x1, framework[0].get_bottom()[1]-0.1, 0], [x1, db[0].get_top()[1]+0.1, 0])
        x2 = framework[0].get_center()[0] + 0.4
        a_df = create_straight_arrow([x2, db[0].get_top()[1]+0.1, 0], [x2, framework[0].get_bottom()[1]-0.1, 0])
        a_cd = create_straight_arrow([content[0].get_left()[0]-0.1, db[0].get_center()[1], 0], [db[0].get_right()[0]+0.1, db[0].get_center()[1], 0])

        # --- 3. Initial Animation Sequence ---
        self.play(Write(title))
        self.play(LaggedStart(FadeIn(client), FadeIn(framework), FadeIn(db), FadeIn(llm), FadeIn(content), FadeIn(fine_tuning), Create(ft_connector), lag_ratio=0.1), run_time=1)
        self.play(Create(a_cd), Create(a_cf), Create(a_fd), Create(a_df), Create(a_fl), Create(a_lf), Create(a_fc), run_time=2)
        self.wait(1)

        # --- 4. EXPANSION: Transition & Chunking View ---
        to_fade = VGroup(client, framework, llm, fine_tuning, ft_connector, a_cf, a_fc, a_fl, a_lf, a_fd, a_df, a_cd, title)
        self.play(FadeOut(to_fade), run_time=1.0)
        
        target_content_pos = LEFT * 4.8
        target_db_pos = RIGHT * 4.8

        # Move Content & DB to focus areas
        self.play(content.animate.move_to(target_content_pos).scale(1.4), db.animate.move_to(target_db_pos), run_time=1.5)

        # Define Chunks (circles replacing the doc/file shapes)
        chunks = VGroup()
        for doc in content[0][0]: # Documents -> Red
            chunks.add(Circle(radius=0.12, color=CHUNK_RED, fill_opacity=1, stroke_width=0).move_to(doc.get_center()))
        for file in content[0][1]: # Files -> Blue
            chunks.add(Circle(radius=0.12, color=CHUNK_BLUE, fill_opacity=1, stroke_width=0).move_to(file.get_center()))

        chunk_label = Text("documents convert into small chunks", font_size=18, color=TEXT_COLOR).next_to(chunks, DOWN, buff=0.8)
        
        # Define Vectorization components
        vector_text = Text("[ 1.1, 2.2, -0.5, ... ]", font_size=28, color=TEXT_COLOR).move_to(ORIGIN)
        vector_label = Text("chunks convert into vectors", font_size=18, color=TEXT_COLOR).next_to(vector_text, DOWN, buff=0.8)
        
        # Fixing the arrow to be strictly horizontal by aligning the y-axis
        arrow_y = chunks.get_center()[1]
        arrow_to_vector = Arrow(
            start=[chunks.get_right()[0] + 0.2, arrow_y, 0], 
            end=[vector_text.get_left()[0] - 0.2, arrow_y, 0], 
            color=ICON_BASE_COLOR, 
            buff=0,
            stroke_width=4
        )

        # Transformation Animation: Icons -> Chunks, then Chunks -> Vectors
        self.play(
            ReplacementTransform(content[0], chunks),
            FadeOut(content[1]), FadeOut(content[2]), 
            Write(chunk_label),
            run_time=1.5
        )
        self.play(
            Create(arrow_to_vector),
            Write(vector_text),
            Write(vector_label),
            run_time=1.5
        )
        self.wait(1)

        # --- 5. 3D Embedding Space ---
        grid_cube_frame, pos_dots_3d, neg_dots_3d = get_3d_grid_cube()
        grid_cube_group = VGroup(grid_cube_frame, pos_dots_3d, neg_dots_3d).move_to(target_db_pos)
        
        # Horizontal arrow to the 3D grid
        arrow_to_cube = Arrow(
            start=[vector_text.get_right()[0] + 0.2, arrow_y, 0], 
            end=[grid_cube_frame.get_left()[0] - 0.2, arrow_y, 0], 
            color=ICON_BASE_COLOR, 
            buff=0,
            stroke_width=4
        )

        self.play(FadeOut(db), run_time=0.5)
        self.play(
            FadeIn(grid_cube_frame), 
            FadeIn(pos_dots_3d), 
            FadeIn(neg_dots_3d), 
            Create(arrow_to_cube),
            run_time=1
        )

        # Move Camera to 3D perspective
        self.move_camera(phi=65 * DEGREES, theta=-35 * DEGREES, run_time=2)

        # 3D Clustering Animation
        cluster_pos = target_db_pos + np.array([0.6, 0.6, 0.6])
        cluster_neg = target_db_pos + np.array([-0.6, -0.6, -0.6])
        
        self.play(
            *[dot.animate.move_to(cluster_pos + np.array([random.uniform(-0.2, 0.2) for _ in range(3)])) for dot in pos_dots_3d],
            *[dot.animate.move_to(cluster_neg + np.array([random.uniform(-0.2, 0.2) for _ in range(3)])) for dot in neg_dots_3d],
            run_time=3
        )
        
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)

from manim import *

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
BACKGROUND_COLOR = WHITE       # White background
CARD_BG = "#fce7f3"            # Very Light Pink

class InformationChaosSceneFixed(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- 1. Chat Interface Setup (Fixed Text Wrapping) ---
        chat_box = RoundedRectangle(
            corner_radius=0.2, height=1.8, width=10, 
            color=PRIMARY_COLOR, stroke_width=2
        ).to_edge(UP, buff=0.4)
        
        user_icon = Circle(radius=0.25, color=PRIMARY_COLOR, fill_opacity=1).move_to(chat_box.get_left() + RIGHT * 0.6)
        
        # Wrapped text to prevent out-of-bounds
        question_content = "“I work remotely. Can I expense a $1,200 monitor\nthat I use for my work?”"
        question_text = Text(
            question_content,
            font_size=22, color=TEXT_COLOR, slant=ITALIC, line_spacing=1.2
        ).next_to(user_icon, RIGHT, buff=0.4)
        
        self.play(Create(chat_box), FadeIn(user_icon))
        self.play(Write(question_text), run_time=1.5)

        # --- 2. Information Cards Helper ---
        def get_info_card(title, content, doc_type, position):
            card_bg = RoundedRectangle(
                corner_radius=0.1, height=2.4, width=2.8, 
                fill_color=CARD_BG, fill_opacity=1, stroke_color=PRIMARY_COLOR, stroke_width=1.5
            )
            header_text = Text(title, font_size=16, color=ACCENT_COLOR, weight=BOLD).shift(UP * 0.8)
            type_label = Text(f"({doc_type})", font_size=11, color=TEXT_COLOR).next_to(header_text, DOWN, buff=0.1)
            body_text = Text(
                content, font_size=13, color=TEXT_COLOR, 
                line_spacing=0.9, t2c={"$1,000": ACCENT_COLOR, "$800": ACCENT_COLOR}
            ).shift(DOWN * 0.4)
            return VGroup(card_bg, header_text, type_label, body_text).move_to(position)

        # --- 3. Layout Positioning (Wide Gap) ---
        card1 = get_info_card("Expense Policy", "Office devices\nup to $1,000\nrequires\napproval.", "PDF", LEFT * 4.8 + DOWN * 0.8)
        card2 = get_info_card("HR Addendum", "Remote staff\nmay expense\nequipment\nonce/year.", "Word", LEFT * 1.6 + DOWN * 0.8)
        card3 = get_info_card("Finance Email", "Monitor costs\nabove $800\ntemporarily\npaused.", "Text", RIGHT * 1.6 + DOWN * 0.8)
        card4 = get_info_card("Employee Data", "Role: Staff\nStatus: Remote\nID: 4042", "DB", RIGHT * 4.8 + DOWN * 0.8)

        # --- 4. Animation Sequence ---
        self.play(LaggedStart(*[FadeIn(c, shift=UP) for c in [card1, card2, card3, card4]], lag_ratio=0.2))
        self.wait(1)

        # Positioning "!" and Warning Text side-by-side
        caution_icon = Text("!", font_size=50, color=PRIMARY_COLOR, weight=BOLD).move_to(DOWN * 2.8 + LEFT * 2.5)
        caution_text = Text("Contradictory Information Detected", font_size=20, color=ACCENT_COLOR).next_to(caution_icon, RIGHT, buff=0.3)
        
        warning_label = VGroup(caution_icon, caution_text).move_to(DOWN * 2.8)

        # Concluding Human Factor Note
        human_note = Text(
            "Written by different people at different times.", 
            font_size=18, color=TEXT_COLOR
        ).to_edge(DOWN, buff=0.2)

        self.play(
            card1[0].animate.set_stroke(color=ACCENT_COLOR, width=4),
            card3[0].animate.set_stroke(color=ACCENT_COLOR, width=4),
            FadeIn(caution_icon, scale=1.2),
            Write(caution_text)
        )
        self.play(Write(human_note))
        self.wait(3)

from manim import *
import numpy as np
import random

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Highlights, Numbers)
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # Black text for white background
ICON_BASE_COLOR = "#ec5599"    # Pinkish base
BACKGROUND_COLOR = WHITE       # White background
LIGHT_PINK = "#fbcfe8"
BLUE_COLOR = "#3b82f6"         # Context/Relevant Docs

class RAGArchitectureSceneGood(Scene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers ---
        def get_number_circle(number):
            circle = Circle(radius=0.15, color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=1)
            num = Text(str(number), color=WHITE, font_size=16, weight=BOLD).move_to(circle)
            return VGroup(circle, num)

        def get_client_icon():
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0).shift(UP * 0.5)
            body = AnnularSector(inner_radius=0, outer_radius=0.5, start_angle=PI, angle=-PI, color=LIGHT_PINK, fill_opacity=1)
            body.stretch(1.2, dim=1).shift(DOWN * 0.15)
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            box = Square(side_length=2.8, color=ICON_BASE_COLOR, stroke_width=2.5)
            sys_text = Paragraph("System prompt = e.g.", "You are a digital assistant", "for our organization...", alignment="center", font_size=12, color=TEXT_COLOR)
            user_text = Text("User prompt (Question)\n\nMost relevant documents", font_size=12, color=PRIMARY_COLOR, weight=BOLD, t2c={"Most relevant documents": BLUE_COLOR})
            text_group = VGroup(sys_text, user_text).arrange(DOWN, buff=0.2).move_to(box.get_center())
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(box, UP, buff=0.1)
            return VGroup(box, text_group, label)

        def get_question_bubble():
            q_str = "Question: I work remotely. Can I\nexpense a $1,200 monitor that\nI use for my work?"
            text = Text(q_str, font_size=12, color=TEXT_COLOR, line_spacing=1.2)
            box = RoundedRectangle(corner_radius=0.2, height=text.height + 0.4, width=text.width + 0.4, color=PRIMARY_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            text.move_to(box)
            return VGroup(box, text)

        def get_response_bubble():
            r_str = "Response: No, you cannot expense a $1,200 monitor\nbecause there is a temporary pause on\nreimbursement requests for computer\nmonitors exceeding $800."
            text = Text(r_str, font_size=12, color=TEXT_COLOR, line_spacing=1.2, slant=ITALIC)
            box = RoundedRectangle(corner_radius=0.2, height=text.height + 0.4, width=text.width + 0.4, color=PRIMARY_COLOR, stroke_width=2, fill_color=LIGHT_PINK, fill_opacity=0.3)
            text.move_to(box)
            return VGroup(box, text)

        def get_db_icon():
            front_sq = Square(side_length=0.9, color=ICON_BASE_COLOR)
            back_sq = Square(side_length=0.9, color=ICON_BASE_COLOR).shift(UP*0.25 + RIGHT*0.25)
            connectors = VGroup(*[Line(front_sq.get_corner(c), back_sq.get_corner(c), color=ICON_BASE_COLOR) for c in [UL, UR, DL, DR]])
            dots = VGroup(*[Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(p) for p in [front_sq.get_center() + LEFT*0.15, back_sq.get_center() + RIGHT*0.15 + UP*0.1, front_sq.get_center() + DOWN*0.15 + RIGHT*0.1]])
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
                corner = Polygon(doc.get_corner(UR), doc.get_corner(UR)+LEFT*0.12, doc.get_corner(UR)+DOWN*0.12+LEFT*0.12, doc.get_corner(UR)+DOWN*0.12, color=color, stroke_width=1.5, fill_color=BACKGROUND_COLOR, fill_opacity=1)
                return VGroup(doc, corner)
            orig_docs = VGroup(*[make_doc(BLUE_COLOR) for _ in range(6)]).arrange_in_grid(rows=2, buff=0.08)
            new_docs = VGroup(*[make_doc(BLUE_COLOR) for _ in range(4)]).arrange_in_grid(rows=2, buff=0.08)
            all_docs = VGroup(orig_docs, new_docs).arrange(RIGHT, buff=0.3)
            orig_label = Text("Top N most", font_size=12, color=BLUE_COLOR).next_to(orig_docs, DOWN, buff=0.1)
            new_label = Text("relevant documents", font_size=12, color=BLUE_COLOR).next_to(new_docs, DOWN, buff=0.1)
            return VGroup(all_docs, orig_label, new_label)

        def create_straight_arrow(start_point, end_point, color=ICON_BASE_COLOR):
            return Line(start=start_point, end=end_point, color=color, stroke_width=3).add_tip(tip_length=0.2, tip_width=0.2)

        # --- Architecture Setup ---
        framework = get_framework_icon().shift(UP*0.5) 
        client = get_client_icon().next_to(framework, LEFT, buff=2.5).shift(UP*0.5)
        question_bubble = get_question_bubble().next_to(client, DOWN, buff=0.5)
        response_bubble = get_response_bubble().next_to(question_bubble, DOWN, buff=0.2)
        llm = get_llm_icon().next_to(framework, RIGHT, buff=2.0).shift(DOWN*0.2)
        db = get_db_icon().next_to(framework, DOWN, buff=1.8)
        content = get_content_icons().next_to(db, RIGHT, buff=1.0).align_to(db, DOWN)
        fine_tuning = get_fine_tuning_icon().next_to(llm, UP, buff=0.4)
        ft_connector = DashedLine(start=fine_tuning.get_bottom(), end=llm.get_top(), color=ICON_BASE_COLOR, stroke_width=2, dash_length=0.1)

        scene_center = VGroup(client, framework, llm, db, content, question_bubble, response_bubble).get_center()
        VGroup(client, framework, llm, db, content, fine_tuning, ft_connector, question_bubble, response_bubble).shift(-scene_center)

        # Arrows & Labels Logic
        arrow_c_f = create_straight_arrow([client[0].get_right()[0] + 0.1, client[0].get_center()[1] - 0.2, 0], [framework[0].get_left()[0] - 0.1, client[0].get_center()[1] - 0.2, 0])
        arrow_f_c = create_straight_arrow([framework[0].get_left()[0] - 0.1, client[0].get_center()[1] + 0.5, 0], [client[0].get_right()[0] + 0.1, client[0].get_center()[1] + 0.5, 0])
        arrow_f_llm = create_straight_arrow([framework[0].get_right()[0] + 0.1, framework[0].get_center()[1] - 0.2, 0], [llm[0].get_left()[0] - 0.1, framework[0].get_center()[1] - 0.2, 0])
        arrow_llm_f = create_straight_arrow([llm[0].get_left()[0] - 0.1, framework[0].get_center()[1] + 0.6, 0], [framework[0].get_right()[0] + 0.1, framework[0].get_center()[1] + 0.6, 0])
        arrow_f_db = create_straight_arrow([framework[0].get_center()[0] - 0.5, framework[0].get_bottom()[1] - 0.1, 0], [framework[0].get_center()[0] - 0.5, db[0].get_top()[1] + 0.1, 0])
        arrow_db_f = create_straight_arrow([framework[0].get_center()[0] + 0.5, db[0].get_top()[1] + 0.1, 0], [framework[0].get_center()[0] + 0.5, framework[0].get_bottom()[1] - 0.1, 0])
        arrow_content_db = create_straight_arrow([content[0].get_left()[0] - 0.1, db[0].get_center()[1], 0], [db[0].get_right()[0] + 0.1, db[0].get_center()[1], 0])

        label_q = Text("Question", font_size=16, color=TEXT_COLOR, slant=ITALIC).move_to(arrow_c_f.get_center()).shift(DOWN * 0.25)
        num_1 = get_number_circle(1).next_to(label_q, LEFT, buff=0.1)
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR, slant=ITALIC).move_to(arrow_f_c.get_center()).shift(UP * 0.25)
        label_sem = Text("Semantic\nSearch", font_size=14, color=TEXT_COLOR, line_spacing=1).move_to(arrow_f_db.get_center()).shift(LEFT * 0.6)
        num_2 = get_number_circle(2).next_to(label_sem, DOWN, buff=0.1)
        label_ctx = Text("Contextual\nData", font_size=14, color=BLUE_COLOR, line_spacing=1).move_to(arrow_db_f.get_center()).shift(RIGHT * 0.6)
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR).move_to(arrow_f_llm.get_center()).shift(DOWN * 0.25)
        num_3 = get_number_circle(3).next_to(label_prompt, DOWN, buff=0.1)
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).move_to(arrow_llm_f.get_center()).shift(UP * 0.25)
        num_4 = get_number_circle(4).next_to(label_post, UP, buff=0.1)

        # Initial Architecture View
        self.add(client, framework, llm, fine_tuning, ft_connector, db, content, question_bubble, response_bubble)
        self.add(arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f, arrow_f_db, arrow_db_f, arrow_content_db)
        self.add(label_q, num_1, label_resp, label_sem, num_2, label_ctx, label_prompt, num_3, label_post, num_4)
        self.wait(1)

        # --- Transition Setup ---
        to_fade = VGroup(
            client, framework, llm, db, fine_tuning, ft_connector, question_bubble, response_bubble,
            arrow_c_f, arrow_f_c, arrow_f_llm, arrow_llm_f, arrow_f_db, arrow_db_f, arrow_content_db,
            label_q, num_1, label_resp, label_sem, num_2, label_ctx, label_prompt, num_3, label_post, num_4,
            content[0][0][1:], content[0][1], content[1], content[2]
        )
        
        survivor_doc = content[0][0][0] # Morph this document icon
        title_text = Text("Challenges in Large Enterprise", font_size=32, color=TEXT_COLOR, weight=BOLD)
        target_icon_rect = Rectangle(height=0.4, width=0.28, color=BLUE_COLOR, stroke_width=1.5)
        exclamation = Text("!", font_size=20, color=BLUE_COLOR, weight=BOLD).move_to(target_icon_rect)
        target_icon = VGroup(target_icon_rect, exclamation)
        target_vgroup = VGroup(target_icon, title_text).arrange(RIGHT, buff=0.4).to_edge(UP, buff=1.0)

        # --- Transition Playback ---
        self.play(FadeOut(to_fade), run_time=1.5)
        self.wait(0.2)

        # Morph survivor doc into the rectangle and write exclamation mark with title
        self.play(
            ReplacementTransform(survivor_doc, target_icon_rect),
            Write(exclamation),
            Write(title_text),
            run_time=1.5
        )
        self.wait(0.5)

        # Bullet Points List
        def get_bullet_entry(text_content):
            dot = Dot(color=PRIMARY_COLOR, radius=0.1)
            txt = Text(text_content, font_size=20, color=TEXT_COLOR, line_spacing=1.5)
            return VGroup(dot, txt).arrange(RIGHT, buff=0.4)

        b1 = get_bullet_entry("Fragmentation: HR vs Finance vs Policy contradictions")
        b2 = get_bullet_entry("Information Drift: Policies changing every single month")
        b3 = get_bullet_entry("Security: Access levels varying by department and seniority")
        
        bullets = VGroup(b1, b2, b3).arrange(DOWN, aligned_edge=LEFT, buff=0.8).next_to(target_vgroup, DOWN, buff=1.2)
        
        for bullet in bullets:
            self.play(FadeIn(bullet[0], scale=0.5), Write(bullet[1]), run_time=1.2)
            self.wait(0.8)

        self.wait(3)

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # Black text
ICON_BASE_COLOR = "#ec5599"    # Pinkish base
BACKGROUND_COLOR = WHITE       # White background
GRID_COLOR = "#d3d4d6"         # Light grey for 3D axes
VECTOR_GREEN = "#10b981"       # Emerald for numerical data
DOC_COLOR = "#3b82f6"          # Blue color for the survivor document

class VectorDatabaseMorphScene(ThreeDScene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers ---
        def get_survivor_doc(color=DOC_COLOR):
            """Stylized document icon used as a visual anchor."""
            doc = Rectangle(height=0.4, width=0.28, color=color, stroke_width=1.5)
            # Folded corner detail
            corner = Polygon(
                doc.get_corner(UR), 
                doc.get_corner(UR) + LEFT * 0.1, 
                doc.get_corner(UR) + DOWN * 0.1 + LEFT * 0.1, 
                doc.get_corner(UR) + DOWN * 0.1, 
                color=color, stroke_width=1.5, fill_color=BACKGROUND_COLOR, fill_opacity=1
            )
            return VGroup(doc, corner)

        # --- Recreate the Challenges Scene ---
        title_text = Text("Challenges in Large Enterprise", font_size=32, color=TEXT_COLOR, weight=BOLD)
        
        # Position the survivor doc icon next to the title
        survivor_doc = get_survivor_doc().scale(1.2)
        
        header_group = VGroup(survivor_doc, title_text).arrange(RIGHT, buff=0.4).to_edge(UP, buff=1.0)
        
        dots = VGroup(
            Dot(color=PRIMARY_COLOR, radius=0.12),
            Dot(color=PRIMARY_COLOR, radius=0.12),
            Dot(color=PRIMARY_COLOR, radius=0.12)
        )
        
        texts = VGroup(
            Text("Fragmentation: HR vs Finance vs Policy contradictions", font_size=20, color=TEXT_COLOR),
            Text("Information Drift: Policies changing every single month", font_size=20, color=TEXT_COLOR),
            Text("Security: Access levels varying by department and seniority", font_size=20, color=TEXT_COLOR)
        )

        bullets = VGroup(
            VGroup(dots[0], texts[0]).arrange(RIGHT, buff=0.4),
            VGroup(dots[1], texts[1]).arrange(RIGHT, buff=0.4),
            VGroup(dots[2], texts[2]).arrange(RIGHT, buff=0.4)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(ORIGIN)
        
        self.add(header_group, bullets)
        self.wait(1)

        # --- Phase 1: Clean Fadeout (Stationary Doc and Text together) ---
        self.play(
            FadeOut(title_text),
            FadeOut(texts),
            FadeOut(survivor_doc), # Now fades out with the header text
            run_time=1.0
        )
        self.wait(0.2)

        # --- Phase 2: Morphing into the Vector Database ---
        db_box = Cube(side_length=3.0, fill_opacity=0, stroke_color=ICON_BASE_COLOR, stroke_width=2)
        db_axes = ThreeDAxes(
            x_range=[-1, 1], y_range=[-1, 1], z_range=[-1, 1],
            x_length=3.0, y_length=3.0, z_length=3.0,
            axis_config={"stroke_width": 1, "color": GRID_COLOR}
        )

        # Fixed UI Elements
        solution_text = Text("Optimized for Meaning, Not Just Text", font_size=24, color=TEXT_COLOR)
        db_label = Text("Vector Database", font_size=28, color=ACCENT_COLOR, weight=BOLD)
        
        self.add_fixed_in_frame_mobjects(solution_text, db_label)
        solution_text.to_edge(UP, buff=0.8)
        db_label.to_edge(DOWN, buff=1.2)

        # Morph 2D dots into 3D Spheres
        spheres = VGroup(*[
            Sphere(radius=0.12, resolution=(10, 10)).set_color(ACCENT_COLOR)
            for _ in range(3)
        ])
        
        target_pos = [
            np.array([0.8, 0.6, 0.4]),
            np.array([-0.6, -0.7, 0.5]),
            np.array([0.2, -0.4, -0.8])
        ]

        # Animation: Transition into the database
        self.play(
            Write(solution_text),
            Create(db_box),
            Create(db_axes),
            Write(db_label),
            ReplacementTransform(dots[0], spheres[0].move_to(target_pos[0])),
            ReplacementTransform(dots[1], spheres[1].move_to(target_pos[1])),
            ReplacementTransform(dots[2], spheres[2].move_to(target_pos[2])),
            run_time=2.5
        )

        # --- Phase 3: Perspective Change ---
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.wait(0.5)

        # --- Phase 4: Numerical Representation ---
        vector_math = MathTex(
            r"", 
            color=VECTOR_GREEN, font_size=32
        )
        self.add_fixed_in_frame_mobjects(vector_math)
        vector_math.to_corner(UL, buff=1.0)

        self.play(Write(vector_math), run_time=1.5)

        # Final Speed Emphasis
        speed_label = Text("Speed of ChatGPT at Scale", font_size=22, color=PRIMARY_COLOR, weight=BOLD)
        self.add_fixed_in_frame_mobjects(speed_label)
        speed_label.next_to(db_label, DOWN, buff=0.2)

        self.play(Write(speed_label), run_time=1)

        # Ambient rotation
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)

from manim import *
import numpy as np
import random

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = "#1f2937"         # Dark Grey/Black for text
ICON_BASE_COLOR = "#ec5599"    # Pinkish base
BACKGROUND_COLOR = WHITE       # White background
GRID_COLOR = "#e5e7eb"         # Light grey for 3D axes
VECTOR_GREEN = "#10b981"       # Emerald for numerical data

class SemanticSearchScene(ThreeDScene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers ---
        def get_db_cube():
            axes = ThreeDAxes(
                x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], z_range=[-1.5, 1.5],
                x_length=4, y_length=4, z_length=4,
                axis_config={"stroke_width": 1, "color": GRID_COLOR}
            )
            cube = Cube(side_length=4, fill_opacity=0, stroke_color=ICON_BASE_COLOR, stroke_width=2)
            return VGroup(axes, cube)

        # --- 2. Initial Layout ---
        title = Text("Semantic Search & Vector Stores", font_size=32, color=BLACK, weight=NORMAL)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)

        db_group = get_db_cube().move_to(ORIGIN)
        
        # Data points (Spheres) representing stored unstructured data
        data_points = VGroup(*[
            Sphere(radius=0.1, resolution=(10, 10)).set_color(ACCENT_COLOR).move_to([
                random.uniform(-1.5, 1.5), 
                random.uniform(-1.5, 1.5), 
                random.uniform(-1.5, 1.5)
            ]) for _ in range(12)
        ])

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(db_group, data_points)
        self.wait(1)

        # --- 3. The User Query ---
        query_text = Text("“How do I expense a monitor?”", font_size=24, color=TEXT_COLOR, slant=ITALIC)
        self.add_fixed_in_frame_mobjects(query_text)
        query_text.to_edge(LEFT, buff=1.0).shift(UP * 1.5)

        # Vectorization of Query
        query_vector_label = MathTex(r"\vec{v}_{query} = [0.42, -0.11, \dots]", color=VECTOR_GREEN, font_size=30)
        self.add_fixed_in_frame_mobjects(query_vector_label)
        query_vector_label.next_to(query_text, DOWN, buff=0.3)

        self.play(Write(query_text))
        self.wait(0.5)
        self.play(Write(query_vector_label))

        # Query point appearing in the vector space
        query_point = Sphere(radius=0.15, resolution=(12, 12)).set_color(PRIMARY_COLOR)
        query_point.move_to([0.5, 0.5, 0.5]) # The "semantic location" of the question

        self.play(FadeIn(query_point, scale=0.5))
        self.wait(0.5)

        # --- 4. Semantic Search (Distance Calculation) ---
        # Find the 3 closest points
        distances = []
        for p in data_points:
            dist = np.linalg.norm(p.get_center() - query_point.get_center())
            distances.append((dist, p))
        
        distances.sort(key=lambda x: x[0])
        closest_points = [d[1] for d in distances[:3]]

        search_lines = VGroup()
        for cp in closest_points:
            line = DashedLine(query_point.get_center(), cp.get_center(), color=PRIMARY_COLOR, stroke_width=2)
            search_lines.add(line)

        semantic_label = Text("Finding Semantic Neighbors", font_size=20, color=PRIMARY_COLOR)
        self.add_fixed_in_frame_mobjects(semantic_label)
        semantic_label.next_to(query_vector_label, DOWN, buff=1.0)

        self.play(
            Create(search_lines),
            Write(semantic_label),
            *[cp.animate.set_color(PRIMARY_COLOR).scale(1.2) for cp in closest_points],
            run_time=2
        )
        self.wait(1)

        # --- 5. Conclusion: The Vector Store ---
        store_alias = Text("Also known as a 'Vector Store'", font_size=24, color=ACCENT_COLOR, weight=BOLD)
        self.add_fixed_in_frame_mobjects(store_alias)
        store_alias.to_edge(DOWN, buff=1.0)

        self.play(
            FadeOut(semantic_label),
            Write(store_alias),
            db_group[1].animate.set_stroke(color=PRIMARY_COLOR, width=4)
        )

        # Final Ambient Rotation to show search context
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = "#1f2937"         # Dark Grey/Black for text
ICON_BASE_COLOR = "#ec5599"    # Pinkish base
BACKGROUND_COLOR = WHITE       # White background
GRID_COLOR = "#e5e7eb"         # Light grey for 3D axes
LINE_COLOR = "#3b82f6"         # Blue for semantic connection

class VectorStoreDefinitionScene(ThreeDScene):
    def construct(self):
        # 1. Setup Background and Camera
        self.camera.background_color = BACKGROUND_COLOR
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # --- Component Helpers ---
        def get_db_cube():
            axes = ThreeDAxes(
                x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], z_range=[-1.5, 1.5],
                x_length=4, y_length=4, z_length=4,
                axis_config={"stroke_width": 1, "color": GRID_COLOR}
            )
            cube = Cube(side_length=4, fill_opacity=0, stroke_color=ICON_BASE_COLOR, stroke_width=2)
            return VGroup(axes, cube)

        # --- 2. Initial Layout (The "Three Balls" State) ---
        db_group = get_db_cube().move_to(ORIGIN)
        
        # Coordinates from the previous morphing sequence
        target_pos = [
            np.array([0.8, 0.6, 0.4]),
            np.array([-0.6, -0.7, 0.5]),
            np.array([0.2, -0.4, -0.8])
        ]
        
        spheres = VGroup(*[
            Sphere(radius=0.12, resolution=(10, 10)).set_color(ACCENT_COLOR).move_to(pos)
            for pos in target_pos
        ])

        # Title (BLACK, NOT BOLD as per requirements)
        title = Text("What is a Vector Database?", font_size=32, color=BLACK)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)

        self.add(db_group, spheres)
        self.wait(1)

        # --- 3. Connecting the Points (Semantic Relationships) ---
        connections = VGroup(
            DashedLine(spheres[0].get_center(), spheres[1].get_center(), color=LINE_COLOR),
            DashedLine(spheres[1].get_center(), spheres[2].get_center(), color=LINE_COLOR),
            DashedLine(spheres[2].get_center(), spheres[0].get_center(), color=LINE_COLOR)
        )

        semantic_text = Text(
            "Enables search across unstructured data", 
            font_size=20, color=TEXT_COLOR
        )
        self.add_fixed_in_frame_mobjects(semantic_text)
        semantic_text.next_to(title, DOWN, buff=0.3)

        self.play(
            Create(connections),
            Write(semantic_text),
            run_time=2
        )
        self.wait(1)

        # --- 4. The Vector Store Alias (Lowered and Reduced) ---
        # Reduced font size and height/width of the box
        alias_box = RoundedRectangle(
            corner_radius=0.1, height=0.7, width=3.2, 
            color=PRIMARY_COLOR, fill_color=WHITE, fill_opacity=1
        )
        alias_text = Text("Vector Store", font_size=24, color=PRIMARY_COLOR, weight=BOLD)
        alias_group = VGroup(alias_box, alias_text).move_to(ORIGIN)
        
        # Adding to fixed frame so it doesn't tilt with the camera
        self.add_fixed_in_frame_mobjects(alias_group)
        
        #buff=0.4 moves it significantly lower to the edge, avoiding the cube
        alias_group.to_edge(DOWN, buff=0.4)

        self.play(
            FadeIn(alias_group, shift=UP),
            spheres.animate.set_color(PRIMARY_COLOR),
            db_group[1].animate.set_stroke(color=PRIMARY_COLOR, width=4),
            run_time=1.5
        )

        # Final rotation to show depth without overlapping text
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(6)
from manim import *
import numpy as np

# ==============================================================================
# GLOBAL COLOR PALETTE & DESIGN CONSTANTS
# ==============================================================================
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # Black text
GRID_COLOR = "#e5e7eb"         # Light grey for UI borders
CODE_BG = "#f3f4f6"            # Light grey for code box
BACKGROUND_COLOR = WHITE       # Clean professional background

# Refined Spacing & Scaling Constants
TABLE_X_OFFSET = -5.4          
TABLE_Y_START = 0.5            
CUBE_X_OFFSET = 0.8            # Shifted left to avoid UI collision
ROW_BUFF = 0.6                 

class CRUDVectorOperationsScene(ThreeDScene):
    """
    Expert AI Explainer: Vector CRUD Lifecycle.
    
    Refined Layout: 
    - Shrunken and lowered SQL Box.
    - CRUD list pinned to the far right.
    - Cube shifted left to ensure no overlaps.
    """

    def construct(self):
        # 0. Initial Scene Configuration
        self.camera.background_color = BACKGROUND_COLOR
        self.set_camera_orientation(phi=75 * DEGREES, theta=-35 * DEGREES)

        # ---------------------------------------------------------
        # COMPONENT HELPERS
        # ---------------------------------------------------------
        
        def create_table_header():
            h1 = Text("ID", font_size=14, color=TEXT_COLOR, weight=BOLD)
            h2 = Text("Vector Embedding", font_size=14, color=TEXT_COLOR, weight=BOLD)
            header_group = VGroup(h1, h2).arrange(RIGHT, buff=0.8)
            line = Line(LEFT*1.8, RIGHT*1.8, color=GRID_COLOR, stroke_width=1.5)
            return VGroup(header_group, line).arrange(DOWN, buff=0.15)

        def create_table_row(uid, vector_str, color=TEXT_COLOR):
            id_text = Text(uid, font_size=12, color=color)
            vec_text = Text(vector_str, font_size=12, color=color)
            row = VGroup(id_text, vec_text).arrange(RIGHT, buff=1.2)
            id_text.align_to(row, LEFT)
            return row

        def create_code_box():
            # Decreased size: width 4.2, height 1.0
            bg = RoundedRectangle(
                corner_radius=0.1, 
                height=1.0, 
                width=4.2, 
                color=GRID_COLOR, 
                fill_color=CODE_BG, 
                fill_opacity=1
            )
            # Smaller font_size for better fit
            query = Text(
                "SELECT * FROM documents\nWHERE similarity(vector, query) > 0.8",
                font_size=11,
                color=TEXT_COLOR,
                line_spacing=0.8
            ).move_to(bg)
            return VGroup(bg, query)

        # ---------------------------------------------------------
        # PHASE 1: INITIAL UI SETUP (Fixed 2D Frame)
        # ---------------------------------------------------------
        
        # 1.1 Main Title - Black and Normal Weight
        main_title = Text("API & CRUD Operations", font_size=28, color=BLACK, weight=NORMAL)
        main_title.to_edge(UP, buff=0.4)
        
        # 1.2 SQL Code Block (Top Right - Moved Downward)
        sql_box = create_code_box().to_edge(UR, buff=0.5).shift(DOWN * 0.6)
        
        # 1.3 CRUD Acronym List (Right Side - Pinned to edge to avoid Cube)
        crud_items = VGroup(
            Text("C - Create", font_size=19, color=TEXT_COLOR, t2c={"C": PRIMARY_COLOR}),
            Text("R - Read", font_size=19, color=TEXT_COLOR, t2c={"R": PRIMARY_COLOR}),
            Text("U - Update", font_size=19, color=TEXT_COLOR, t2c={"U": PRIMARY_COLOR}),
            Text("D - Delete", font_size=19, color=TEXT_COLOR, t2c={"D": PRIMARY_COLOR}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(sql_box, DOWN, buff=0.7).to_edge(RIGHT, buff=0.5)

        # 1.4 Table Setup (Left Side)
        table_header = create_table_header().move_to([TABLE_X_OFFSET + 1.2, TABLE_Y_START + 0.8, 0])
        row1 = create_table_row("ax0", "[0.002, -0.5, ...]").move_to([TABLE_X_OFFSET + 1.2, TABLE_Y_START, 0])
        row2 = create_table_row("ax2", "[-0.001, 0.45, ...]").move_to([TABLE_X_OFFSET + 1.2, TABLE_Y_START - ROW_BUFF, 0])
        active_table_rows = VGroup(row1, row2)

        self.add_fixed_in_frame_mobjects(main_title, sql_box, crud_items, table_header, active_table_rows)

        # ---------------------------------------------------------
        # PHASE 2: 3D VECTOR SPACE SETUP
        # ---------------------------------------------------------
        
        db_axes = ThreeDAxes(
            x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], z_range=[-1.5, 1.5],
            x_length=2.8, y_length=2.8, z_length=2.8,
            axis_config={"stroke_width": 1, "color": GRID_COLOR}
        ).move_to([CUBE_X_OFFSET, -0.2, 0])

        db_cube = Cube(
            side_length=2.8, fill_opacity=0.03, fill_color=PRIMARY_COLOR, 
            stroke_color=PRIMARY_COLOR, stroke_width=1
        ).move_to(db_axes)

        p1 = Sphere(radius=0.1).set_color(ACCENT_COLOR).move_to(db_axes.c2p(0.12, -0.5, 0.8))
        p2 = Sphere(radius=0.1).set_color(ACCENT_COLOR).move_to(db_axes.c2p(-0.8, 0.4, -0.3))
        active_spheres = VGroup(p1, p2)

        self.play(
            FadeIn(db_axes), Create(db_cube),
            FadeIn(active_spheres),
            Write(crud_items),
            FadeIn(sql_box, shift=DOWN * 0.2),
            run_time=1.5
        )

        # ---------------------------------------------------------
        # PHASE 3: CRUD OPERATIONS
        # ---------------------------------------------------------

        # --- CREATE ---
        self.play(Indicate(crud_items[0], color=PRIMARY_COLOR))
        new_row = create_table_row("ax3", "[0.887, -0.22, ...]").move_to([TABLE_X_OFFSET + 1.2, TABLE_Y_START - 2*ROW_BUFF, 0])
        new_p = Sphere(radius=0.1).set_color(PRIMARY_COLOR).move_to(db_axes.c2p(0.6, 0.9, -0.2))
        self.add_fixed_in_frame_mobjects(new_row)
        
        self.play(FadeIn(new_row, shift=RIGHT), FadeIn(new_p, scale=0.5), run_time=1.2)
        active_table_rows.add(new_row)
        active_spheres.add(new_p)
        self.wait(1)

        # --- READ ---
        self.play(Indicate(crud_items[1], color=PRIMARY_COLOR), Indicate(sql_box, color=PRIMARY_COLOR))
        self.play(
            active_table_rows.animate.set_color(PRIMARY_COLOR),
            *[s.animate.set_color(PRIMARY_COLOR).scale(1.3) for s in active_spheres],
            run_time=1
        )
        self.wait(0.5)
        self.play(
            active_table_rows.animate.set_color(TEXT_COLOR),
            *[s.animate.set_color(ACCENT_COLOR).scale(1/1.3) for s in active_spheres],
            run_time=1
        )

        # --- UPDATE ---
        self.play(Indicate(crud_items[2], color=PRIMARY_COLOR))
        updated_row_text = create_table_row("ax1", "[0.002, -0.01, ...]").move_to(active_table_rows[0].get_center())
        self.add_fixed_in_frame_mobjects(updated_row_text)
        
        self.play(
            FadeOut(active_table_rows[0], shift=UP * 0.1),
            FadeIn(updated_row_text, shift=UP * 0.1),
            active_spheres[0].animate.move_to(db_axes.c2p(1.2, -1.0, 0.2)).set_color(PRIMARY_COLOR),
            run_time=1.5
        )
        active_table_rows[0] = updated_row_text
        self.wait(1)

        # --- DELETE ---
        self.play(Indicate(crud_items[3], color=PRIMARY_COLOR))
        self.play(
            FadeOut(active_table_rows[1], shift=LEFT), 
            FadeOut(active_spheres[1], scale=0), 
            run_time=1
        )
        self.play(active_table_rows[2].animate.shift(UP * ROW_BUFF), run_time=0.8)
        self.wait(1)

        # ---------------------------------------------------------
        # PHASE 4: AMBIENT ROTATION
        # ---------------------------------------------------------
        
        self.play(FadeOut(crud_items), FadeOut(sql_box), run_time=1)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)

from manim import *

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Header Background
TEXT_COLOR = "#1f2937"         # Standard Text
HEADER_TEXT_COLOR = WHITE      
ROW_BG_ODD = "#f9fafb"         # Light Stripe
BORDER_COLOR = "#9ca3af"       
BACKGROUND_COLOR = WHITE       

class CleanVectorStoreTable(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- 1. Intro Text ---
        intro = Text(
            "Not all vector stores are created equal.\nAs a leader or architect, you’ll likely choose from three categories:",
            font_size=20, color=TEXT_COLOR, line_spacing=1.2
        ).to_edge(UP, buff=0.4)

        # --- 2. Manual Header Construction ---
        # Optimized widths for better text fitting
        col_widths = [2.6, 3.2, 3.8, 3.4]
        header_labels = ["Category", "Examples", "Best For...", "Cons"]
        
        headers = VGroup()
        for label, width in zip(header_labels, col_widths):
            bg = Rectangle(
                width=width, height=0.7, 
                fill_color=PRIMARY_COLOR, fill_opacity=1, 
                stroke_color=BORDER_COLOR, stroke_width=1
            )
            txt = Text(label, font_size=18, weight=BOLD, color=HEADER_TEXT_COLOR).move_to(bg)
            headers.add(VGroup(bg, txt))
        headers.arrange(RIGHT, buff=0)

        # --- 3. The Data Rows ---
        rows_data = [
            ["Managed /\nSpecialized", "Pinecone,\nWeaviate", "Speed to market;\nteams who want\n\"AI-native\" features.", "Can get expensive\nat a massive scale."],
            ["Database\nExtensions", "pgvector\n(Postgres), Elastic", "Organizations wanting\nto keep data in\nexisting infra.", "Performance\nceilings under\nheavy load."],
            ["Cloud Native", "AWS OpenSearch,\nGoogle Vertex", "Deep integration\nwith your existing\ncloud ecosystem.", "Complex setup;\nhigh \"locked-in\"\ncosts."]
        ]

        table_content = VGroup()
        for r_idx, row in enumerate(rows_data):
            row_group = VGroup()
            # Alternating row background for readability
            bg_color = ROW_BG_ODD if r_idx % 2 == 0 else WHITE
            
            for c_idx, cell_text in enumerate(row):
                cell_bg = Rectangle(
                    width=col_widths[c_idx], height=1.6, 
                    fill_color=bg_color, fill_opacity=1, 
                    stroke_color=BORDER_COLOR, stroke_width=1
                )
                
                # First column stays bold, others are normal
                is_bold = BOLD if c_idx == 0 else NORMAL
                cell_txt = Text(
                    cell_text, font_size=15, 
                    color=TEXT_COLOR, weight=is_bold, 
                    line_spacing=1.2
                ).move_to(cell_bg)
                
                row_group.add(VGroup(cell_bg, cell_txt))
            
            row_group.arrange(RIGHT, buff=0)
            table_content.add(row_group)
        
        table_content.arrange(DOWN, buff=0).next_to(headers, DOWN, buff=0)

        # --- 4. Grouping and Final Alignment ---
        full_table = VGroup(headers, table_content).center().shift(DOWN * 0.3)
        intro.next_to(full_table, UP, buff=0.5)

        # --- 5. Animation Sequence ---
        self.play(Write(intro), run_time=1.5)
        self.play(FadeIn(headers, shift=UP), run_time=1)
        
        # Staggered entrance for the rows
        for row in table_content:
            self.play(FadeIn(row, shift=DOWN), run_time=0.7)
            self.wait(0.2)
        
        self.wait(5)

from manim import *

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red for Header
TEXT_COLOR = "#1f2937"         # Dark Grey/Black
HEADER_TEXT_COLOR = WHITE      
ROW_BG_ODD = "#f9fafb"         # Light Stripe
BORDER_COLOR = "#9ca3af"       
BACKGROUND_COLOR = WHITE       

class ComponentResponsibilityTable(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- 1. Header Construction ---
        col_widths = [4.5, 7.5]
        header_labels = ["Component", "Responsibility"]
        
        headers = VGroup()
        for label, width in zip(header_labels, col_widths):
            bg = Rectangle(
                width=width, height=0.8, 
                fill_color=PRIMARY_COLOR, fill_opacity=1, 
                stroke_color=BORDER_COLOR, stroke_width=1
            )
            txt = Text(label, font_size=22, weight=BOLD, color=HEADER_TEXT_COLOR).move_to(bg)
            headers.add(VGroup(bg, txt))
        headers.arrange(RIGHT, buff=0)
        headers.to_edge(UP, buff=1.5)

        # --- 2. Data Rows ---
        rows_data = [
            ["Semantic Search", "How meaning is represented"],
            ["LLM", "How reasoning happens"],
            ["RAG", "How reasoning is grounded"],
            ["Vector DB", "How meaning is stored and retrieved at scale"]
        ]

        table_content = VGroup()
        for r_idx, row in enumerate(rows_data):
            row_group = VGroup()
            bg_color = ROW_BG_ODD if r_idx % 2 == 0 else WHITE
            
            # Vector DB row uses BOLD but no extra color highlighting
            is_vector_db = row[0] == "Vector DB"
            text_weight = BOLD if is_vector_db else NORMAL
            
            for c_idx, cell_text in enumerate(row):
                cell_bg = Rectangle(
                    width=col_widths[c_idx], height=1.2, 
                    fill_color=bg_color, fill_opacity=1, 
                    stroke_color=BORDER_COLOR, stroke_width=1
                )
                
                cell_txt = Text(
                    cell_text, font_size=18, 
                    color=TEXT_COLOR, weight=text_weight
                ).move_to(cell_bg)
                
                # Align text to the left within the cell
                cell_txt.align_to(cell_bg, LEFT).shift(RIGHT * 0.4)
                
                row_group.add(VGroup(cell_bg, cell_txt))
            
            row_group.arrange(RIGHT, buff=0)
            table_content.add(row_group)
        
        table_content.arrange(DOWN, buff=0).next_to(headers, DOWN, buff=0)

        # Center the entire table
        full_table = VGroup(headers, table_content).center()

        # --- 3. Animation Sequence ---
        self.play(FadeIn(headers, shift=UP), run_time=1)
        self.wait(0.2)
        
        for row in table_content:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.6)
        
        # No extra highlight at the end
        self.wait(5)

from manim import *

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = "#1f2937"         # Dark Grey
MEMORY_GLOW = "#f472b6"        # Soft Pink for the "Memory" effect
BACKGROUND_COLOR = WHITE

class OrganizationalMemoryScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- 1. The Central "Organizational Memory" ---
        memory_core = Sphere(radius=0.8, resolution=(20, 20)).set_color(PRIMARY_COLOR)
        memory_label = Text("Organizational Memory", font_size=24, color=PRIMARY_COLOR, weight=BOLD).next_to(memory_core, DOWN, buff=0.4)
        
        # A soft glow effect
        glow = Circle(radius=1.2, color=MEMORY_GLOW, fill_opacity=0.2, stroke_width=0).move_to(memory_core)

        # --- 2. Initial Animation ---
        title = Text("More than just raw text: The Meaning", font_size=28, color=TEXT_COLOR).to_edge(UP, buff=0.5)

        self.play(Write(title))
        self.wait(0.5)

        # Draw the core to represent the start of the "Memory"
        self.play(
            DrawBorderThenFill(memory_core),
            FadeIn(glow),
            run_time=1.5
        )
        self.play(Write(memory_label))
        self.wait(1)

        # --- 3. The "Foundation" Transition ---
        # Instead of icons, we use pulses of light or just the glowing core to represent the meaning
        foundation_title = Text("Critical Foundational Component", font_size=26, color=ACCENT_COLOR, weight=BOLD).move_to(title)

        # Shift the memory core slightly to center it as a foundation
        self.play(
            ReplacementTransform(title, foundation_title),
            memory_core.animate.scale(1.2),
            glow.animate.scale(1.3),
            run_time=1.5
        )

        # Pulse the core to show its active role as a foundation for all AI
        self.play(
            glow.animate.scale(1.5).set_opacity(0.4),
            memory_core.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=2
        )

        self.wait(5)

from manim import *

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red for headers and highlights
TEXT_COLOR = BLACK             # Black text for white background
LABEL_COLOR = "#4b5563"        # Grey for metadata labels
BORDER_COLOR = "#d1d5db"       # Light grey for table lines
BACKGROUND_COLOR = WHITE       # White background

class PDFToVectorTable(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- Phase 1: 100-page PDF Icon ---
        pdf_rect = Rectangle(width=1.8, height=2.5, color=PRIMARY_COLOR, stroke_width=2)
        pdf_label = Text("PDF", font_size=30, weight=NORMAL, color=PRIMARY_COLOR).move_to(pdf_rect.get_top()).shift(DOWN * 0.5)
        pdf_pages = Text("100 Pages", font_size=18, color=TEXT_COLOR).next_to(pdf_label, DOWN, buff=0.4)
        pdf_icon = VGroup(pdf_rect, pdf_label, pdf_pages).center()

        self.play(Create(pdf_icon))
        self.wait(1)

        # --- Phase 2: Breaking into Chunks ---
        chunks = VGroup(*[
            Rectangle(width=0.7, height=0.4, color=PRIMARY_COLOR, fill_opacity=0.2)
            for _ in range(8)
        ]).arrange_in_grid(rows=4, cols=2, buff=0.2).move_to(ORIGIN + UP * 0.5)
        
        chunks_text = Text("Chunks", font_size=24, color=TEXT_COLOR, weight=NORMAL).next_to(chunks, DOWN, buff=0.5)

        self.play(
            ReplacementTransform(pdf_icon, chunks),
            Write(chunks_text),
            run_time=1.5
        )
        self.wait(1)

        # --- Phase 3: Morphing into Chunk IDs (Fixing Overlap) ---
        # Transform rectangles into circles
        circles = VGroup(*[
            Circle(radius=0.15, color=PRIMARY_COLOR, fill_opacity=0.8)
            for _ in range(8)
        ]).arrange_in_grid(rows=4, cols=2, buff=0.5).move_to(chunks.get_center())

        # Labels for the first three circles
        id_labels = VGroup(
            Text("8829-ax1", font_size=18, color=TEXT_COLOR),
            Text("8829-ax2", font_size=18, color=TEXT_COLOR),
            Text("8829-ax3", font_size=18, color=TEXT_COLOR)
        )
        
        # FIX: Position labels to avoid overlap
        # Two labels on the left side of the circles, one on the right side
        id_labels[0].next_to(circles[0], LEFT, buff=0.3)   # Top Left Circle -> Label Left
        id_labels[1].next_to(circles[1], RIGHT, buff=0.3)  # Top Right Circle -> Label Right
        id_labels[2].next_to(circles[2], LEFT, buff=0.3)   # Second Left Circle -> Label Left

        chunk_ids_text = Text("Chunk IDs", font_size=24, color=TEXT_COLOR, weight=NORMAL).move_to(chunks_text)

        self.play(
            ReplacementTransform(chunks, circles),
            Transform(chunks_text, chunk_ids_text),
            run_time=1
        )
        
        # Focus on 3, fade the rest
        self.play(
            circles[3:].animate.set_opacity(0.1),
            FadeIn(id_labels, shift=UP * 0.1),
            run_time=1
        )
        self.wait(2)
        
        # Cleanup for Table Transition
        self.play(
            FadeOut(circles),
            FadeOut(id_labels),
            FadeOut(chunks_text),
            run_time=1
        )

        # --- Phase 4: Detailed Vector Database Table ---
        headers = [
            Text("ID", font_size=20, weight=NORMAL, color=PRIMARY_COLOR),
            Text("Original Text (Chunk)", font_size=20, weight=NORMAL, color=PRIMARY_COLOR),
            Text("Vector Embedding\n(Coordinates)", font_size=20, weight=NORMAL, color=PRIMARY_COLOR),
            Text("Metadata (URL & Ref)", font_size=20, weight=NORMAL, color=PRIMARY_COLOR)
        ]

        def create_metadata(doc, page, date):
            return VGroup(
                Text(f"URL: internal.company.com/finance/handbook#page={page}", font_size=12, color=LABEL_COLOR),
                Text(f"Doc: {doc}", font_size=12, color=LABEL_COLOR),
                Text(f"Page: {page}", font_size=12, color=LABEL_COLOR),
                Text(f"Updated: {date}", font_size=12, color=LABEL_COLOR)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        # Row Data
        row1 = [
            Text("8829-ax1", font_size=18, color=TEXT_COLOR, weight=BOLD),
            Paragraph(
                '"...Remote employees may request reimbursement\nfor home office equipment. Note: As of June 2024,\nthere is a $800 limit on computer monitors..."',
                font_size=16, line_spacing=1.2, color=TEXT_COLOR
            ),
            VGroup(
                Text("[0.0021, -0.0142, 0.5531, -0.2210, ...]", font_size=14, font="Consolas", color=TEXT_COLOR),
                Text("(1536 dimensions total)", font_size=12, color=LABEL_COLOR)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            create_metadata("Home_Office_Policy_V2.pdf", "12", "2024-06-15")
        ]

        row2 = [
            Text("8829-ax2", font_size=18, color=TEXT_COLOR, weight=BOLD),
            Paragraph(
                '"...Any amount exceeding the $800 limit requires\nVP approval. Equipment remains company property\nand must be returned upon termination..."',
                font_size=16, line_spacing=1.2, color=TEXT_COLOR
            ),
            VGroup(
                Text("[-0.0123, 0.4532, -0.1121, 0.0098, ...]", font_size=14, font="Consolas", color=TEXT_COLOR),
                Text("(1536 dimensions total)", font_size=12, color=LABEL_COLOR)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            create_metadata("Home_Office_Policy_V2.pdf", "13", "2024-09-11")
        ]

        row3 = [
            Text("8829-ax3", font_size=18, color=TEXT_COLOR, weight=BOLD),
            Paragraph(
                '"...Internet stipends are processed monthly.\nEmployees must provide proof of high-speed\nconnection for eligibility in the remote program..."',
                font_size=16, line_spacing=1.2, color=TEXT_COLOR
            ),
            VGroup(
                Text("[0.8872, -0.2231, 0.0044, 0.1192, ...]", font_size=14, font="Consolas", color=TEXT_COLOR),
                Text("(1536 dimensions total)", font_size=12, color=LABEL_COLOR)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            create_metadata("Home_Office_Policy_V2.pdf", "15", "2024-07-20")
        ]

        table = MobjectTable(
            [row1, row2, row3],
            col_labels=headers,
            include_outer_lines=True,
            line_config={"color": BORDER_COLOR, "stroke_width": 1.5},
            v_buff=0.5,
            h_buff=0.5
        ).scale_to_fit_width(config.frame_width - 1.0).center()

        self.play(Create(table.get_horizontal_lines()), Create(table.get_vertical_lines()), run_time=1.5)
        self.play(Write(table.get_labels()))
        
        for row in table.get_rows()[1:]:
            self.play(FadeIn(row), run_time=0.8)
        
        self.wait(5)

from manim import *

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      
TEXT_COLOR = BLACK             
LABEL_COLOR = "#4b5563"        
BORDER_COLOR = "#d1d5db"       
SYNC_COLOR = "#f90a75"         
BACKGROUND_COLOR = WHITE       

class DataSynchronizationScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- 1. Layout Anchors ---
        # Positioned to maximize space for the large table
        DIVIDER_X = -3.5
        PDF_X = -5.4
        TABLE_CENTER_X = 2.2 

        div_line = Line(UP*4.0, DOWN*4.0, color=BORDER_COLOR).move_to([DIVIDER_X, 0, 0])
        
        source_label = Text("Source (SharePoint/Web)", font_size=16, color=PRIMARY_COLOR, weight=BOLD).to_edge(UP, buff=0.5).shift(LEFT*5.1)
        db_label = Text("Vector Database", font_size=24, color=PRIMARY_COLOR, weight=BOLD).to_edge(UP, buff=0.4).shift(RIGHT*2.2)

        self.play(Create(div_line), Write(source_label), Write(db_label))

        # --- 2. Source Document ---
        doc_rect = Rectangle(width=2.4, height=3.8, color=BORDER_COLOR, fill_opacity=0.05).move_to([PDF_X, -0.5, 0])
        doc_title = Text("Home_Office_Policy_V2.pdf", font_size=10, color=LABEL_COLOR).next_to(doc_rect, UP, buff=0.1)
        
        policy_text = VGroup(
            Text("Remote employees", font_size=11, color=TEXT_COLOR),
            Text("may request", font_size=11, color=TEXT_COLOR),
            Text("reimbursement for", font_size=11, color=TEXT_COLOR),
            Text("home office", font_size=11, color=TEXT_COLOR),
            Text("equipment.", font_size=11, color=TEXT_COLOR),
            Text("Limit: $800", font_size=11, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(doc_rect.get_center())

        self.play(Create(doc_rect), Write(doc_title), Write(policy_text))

        # --- 3. Vector Database Table ---
        # Column headers in pink
        headers = [
            Text("ID", font_size=16, color=PRIMARY_COLOR, weight=BOLD),
            Text("Original Text", font_size=16, color=PRIMARY_COLOR, weight=BOLD),
            Text("Vector Embedding", font_size=16, color=PRIMARY_COLOR, weight=BOLD),
            Text("Metadata", font_size=16, color=PRIMARY_COLOR, weight=BOLD)
        ]

        # Helper to get row data with fixed font sizes to prevent overflow
        def get_row_data(text_val, vector_str, date_val, text_color=TEXT_COLOR):
            return [
                Text("8829-ax1", font_size=14, color=text_color, weight=BOLD),
                Paragraph(text_val, font_size=12, line_spacing=1.2, color=text_color),
                Text(vector_str, font_size=10, font="Consolas", color=text_color),
                VGroup(
                    Text("Doc: Home_Office_Policy_V2.pdf", font_size=10, color=LABEL_COLOR),
                    Text(f"Updated: {date_val}", font_size=10, color=PRIMARY_COLOR if date_val != "2024-06-15" else LABEL_COLOR)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            ]

        current_row = get_row_data("...limit on\ncomputer monitors\nis $800...", "[0.0021, -0.0142, ...]", "2024-06-15")
        
        # Table with increased buff to prevent out-of-bounds text
        table = MobjectTable(
            [current_row],
            col_labels=headers,
            include_outer_lines=True,
            line_config={"color": BORDER_COLOR, "stroke_width": 2},
            h_buff=0.6, v_buff=0.7
        ).scale(0.85).move_to([TABLE_CENTER_X, -0.5, 0])

        self.play(Create(table))
        self.wait(1)

        # --- 4. Policy Change ---
        strike = Line(policy_text[-1].get_left(), policy_text[-1].get_right(), color=SYNC_COLOR)
        updated_limit = Text("$1200", font_size=12, color=PRIMARY_COLOR, weight=BOLD).next_to(policy_text[-1], DOWN, buff=0.1, aligned_edge=LEFT)

        self.play(Create(strike), FadeIn(updated_limit, shift=UP))

        # --- 5. Sync Notification ---
        sync_arrow = Arrow(start=[DIVIDER_X + 0.2, -0.5, 0], end=[table.get_left()[0] - 0.2, -0.5, 0], color=SYNC_COLOR, stroke_width=4)
        sync_text = Text("Detecting Change", font_size=12, color=SYNC_COLOR).next_to(sync_arrow, UP, buff=0.1)

        self.play(GrowArrow(sync_arrow), Write(sync_text))
        self.wait(0.5)

        # --- 6. Database Update ---
        # Content changes color/value but maintains the same font size
        new_row_data = get_row_data("...limit on\ncomputer monitors\nis $1200...", "[0.0041, -0.0542, ...]", "2026-02-06", text_color=SYNC_COLOR)
        
        new_row_mobjects = VGroup(*[
            table.get_cell((2, i+1)).add(new_row_data[i].move_to(table.get_cell((2, i+1)))) 
            for i in range(4)
        ])

        self.play(
            FadeOut(table.get_rows()[1]),
            FadeIn(new_row_mobjects),
            run_time=1.5
        )

        self.play(FadeOut(sync_arrow), FadeOut(sync_text))
        self.wait(5)

from manim import *

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red
TEXT_COLOR = BLACK             
LABEL_COLOR = "#4b5563"        
BORDER_COLOR = "#d1d5db"       
FILTER_COLOR = "#d56296"       # Blue
SUCCESS_COLOR = "#f10871"      # Green
BACKGROUND_COLOR = WHITE       

class RetrievalFilteringScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- 1. The Vector Database Table ---
        # Defining headers and row data with "Original Text" visible from start
        headers = [
            Text("ID", font_size=14, color=PRIMARY_COLOR, weight=BOLD),
            Text("Original Text", font_size=14, color=PRIMARY_COLOR, weight=BOLD),
            Text("Metadata (Filter)", font_size=14, color=PRIMARY_COLOR, weight=BOLD)
        ]

        row1_data = [
            Text("8829-ax8", font_size=12, color=TEXT_COLOR),
            Paragraph("...senior roles are allowed for expenses......", font_size=12, color=TEXT_COLOR),
            Text("Role: VP_Only", font_size=12, color=LABEL_COLOR)
        ]

        row2_data = [
            Text("8829-ax11", font_size=12, color=TEXT_COLOR),
            Paragraph("800$ limit on computer monitors...", font_size=12, color=TEXT_COLOR),
            Text("Role: ALL", font_size=12, color=LABEL_COLOR)
        ]

        # Use large vertical buffer to resolve overlapping input boxes
        table = MobjectTable(
            [row1_data, row2_data],
            col_labels=headers,
            include_outer_lines=True,
            line_config={"color": BORDER_COLOR},
            h_buff=0.5, 
            v_buff=1.6  
        ).scale(0.85).to_edge(RIGHT, buff=0.8).shift(UP*0.5)

        # --- 2. User Inputs (Left Column) ---
        query_box = RoundedRectangle(corner_radius=0.1, width=4.5, height=1.3, color=BORDER_COLOR)
        query_label = Text("User Query:", font_size=16, color=PRIMARY_COLOR, weight=BOLD).move_to(query_box.get_top()).shift(DOWN*0.3)
        query_text = Text('"Can I expense a $1200 monitor?"', font_size=13, color=TEXT_COLOR).next_to(query_label, DOWN, buff=0.1)
        user_query = VGroup(query_box, query_label, query_text)
        user_query.move_to([ -4.0, table.get_rows()[1].get_center()[1], 0])

        security_box = RoundedRectangle(corner_radius=0.1, width=4.5, height=1.3, color=FILTER_COLOR)
        security_label = Text("Security Context:", font_size=16, color=FILTER_COLOR, weight=BOLD).move_to(security_box.get_top()).shift(DOWN*0.3)
        security_text = Text("User Role: VP of Marketing", font_size=13, color=TEXT_COLOR).next_to(security_label, DOWN, buff=0.1)
        security_context = VGroup(security_box, security_label, security_text)
        security_context.move_to([ -4.0, table.get_rows()[2].get_center()[1], 0])

        self.play(FadeIn(user_query), FadeIn(security_context), FadeIn(table))
        self.wait(1)

        # --- 3. Filtering Logic (Horizontal Flow) ---
        q_arrow = Arrow(user_query.get_right(), table.get_rows()[1].get_left(), color=PRIMARY_COLOR, buff=0.6)
        s_arrow = Arrow(security_context.get_right(), table.get_rows()[2].get_left(), color=FILTER_COLOR, buff=0.6)
        
        filter_msg = Text("Applying Metadata Filter...", font_size=16, color=FILTER_COLOR, weight=BOLD).next_to(table, UP, buff=0.4)

        self.play(GrowArrow(q_arrow), GrowArrow(s_arrow))
        self.play(Write(filter_msg))

        # --- 4. Retrieval & Filtering Result ---
        row_target = table.get_rows()[2]
        cross_line = Line(
            table.get_cell((3,1)).get_left() + RIGHT*0.15, 
            table.get_cell((3,3)).get_right() + LEFT*0.15, 
            color=FILTER_COLOR, 
            stroke_width=6
        ).move_to(row_target.get_center())
        
        self.play(Create(cross_line), row_target.animate.set_opacity(0.2))
        self.play(table.get_rows()[1].animate.set_color(SUCCESS_COLOR))

        # --- 5. LLM Grounding (90 Degree Vertical Arrow) ---
        llm_box = RoundedRectangle(corner_radius=0.1, width=5, height=1.0, color=SUCCESS_COLOR, fill_opacity=0.05)
        llm_label = Text("LLM (Gemini/GPT-4)", font_size=18, color=SUCCESS_COLOR, weight=BOLD).move_to(llm_box.get_center())
        
        # Align LLM card center with the "Original Text" column center
        target_x = table.get_cell((2,2)).get_center()[0]
        llm_group = VGroup(llm_box, llm_label).move_to([target_x, -3.2, 0])

        retrieval_arrow = Arrow(
            start=table.get_cell((2,2)).get_bottom(), 
            end=llm_group.get_top(), 
            color=SUCCESS_COLOR, 
            buff=0.2
        )
        retrieval_text = Text("", font_size=13, color=SUCCESS_COLOR, weight=BOLD).next_to(retrieval_arrow, LEFT, buff=0.2)

        self.play(
            GrowArrow(retrieval_arrow),
            Write(retrieval_text),
            FadeIn(llm_group, shift=UP)
        )

        # AI Result text placed on the LEFT of the LLM card
        ai_bubble = Text('"As a VP of Marketing, you are allowed for that expense."', font_size=14, color=TEXT_COLOR, slant=ITALIC).next_to(llm_group, LEFT, buff=0.5)
        self.play(Write(ai_bubble))

        self.wait(5)

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

class RAGArchitectureScenesGood(Scene):
    def construct(self):
        # 1. Setup Background
        self.camera.background_color = BACKGROUND_COLOR

        # --- Component Helpers ---

        def get_client_icon():
            head = Circle(radius=0.3, color=LIGHT_PINK, fill_color=LIGHT_PINK, fill_opacity=1, stroke_width=0)
            head.shift(UP * 0.5)
            body = AnnularSector(inner_radius=0, outer_radius=0.5, start_angle=PI, angle=-PI, color=LIGHT_PINK, fill_opacity=1)
            body.stretch(1.2, dim=1).shift(DOWN * 0.15)
            icon_group = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon_group, DOWN, buff=0.15)
            return VGroup(icon_group, label)

        def get_framework_icon():
            box = Square(side_length=2.8, color=ICON_BASE_COLOR, stroke_width=2.5)
            sys_text = Paragraph("System prompt = e.g.", "You are a digital assistant", "for our organization...", alignment="center", font_size=12, color=TEXT_COLOR)
            user_text = Text("User prompt (Question)\n\nMost relevant documents", font_size=12, color=PRIMARY_COLOR, weight=BOLD, t2c={"Most relevant documents": BLUE_COLOR})
            text_group = VGroup(sys_text, user_text).arrange(DOWN, buff=0.2).move_to(box.get_center())
            label = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(box, UP, buff=0.1)
            return VGroup(box, text_group, label)

        def get_question_bubble():
            q_str = "Question: I work remotely. Can I\nexpense a $1,200 monitor that\nI use for my work?"
            text = Text(q_str, font_size=12, color=TEXT_COLOR, line_spacing=1.2)
            box = RoundedRectangle(corner_radius=0.2, height=text.height + 0.4, width=text.width + 0.4, color=PRIMARY_COLOR, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            text.move_to(box)
            return VGroup(box, text)

        def get_response_bubble():
            r_str = "Response: No, you cannot expense a $1,200 monitor\nbecause there is a temporary pause on\nreimbursement requests for computer\nmonitors exceeding $800."
            text = Text(r_str, font_size=12, color=TEXT_COLOR, line_spacing=1.2, slant=ITALIC)
            box = RoundedRectangle(corner_radius=0.2, height=text.height + 0.4, width=text.width + 0.4, color=PRIMARY_COLOR, stroke_width=2, fill_color=LIGHT_PINK, fill_opacity=0.3)
            text.move_to(box)
            return VGroup(box, text)

        def get_db_icon():
            front_sq = Square(side_length=0.9, color=ICON_BASE_COLOR)
            back_sq = Square(side_length=0.9, color=ICON_BASE_COLOR).shift(UP*0.25 + RIGHT*0.25)
            connectors = VGroup(*[Line(front_sq.get_corner(c), back_sq.get_corner(c), color=ICON_BASE_COLOR) for c in [UL, UR, DL, DR]])
            dots = VGroup(Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + LEFT*0.15), Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(back_sq.get_center() + RIGHT*0.15 + UP*0.1), Dot(color=ICON_BASE_COLOR, radius=0.05).move_to(front_sq.get_center() + DOWN*0.15 + RIGHT*0.1))
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
                corner = Polygon(doc.get_corner(UR), doc.get_corner(UR)+LEFT*0.12, doc.get_corner(UR)+DOWN*0.12+LEFT*0.12, doc.get_corner(UR)+DOWN*0.12, color=color, stroke_width=1.5, fill_color=BACKGROUND_COLOR, fill_opacity=1)
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
            line = Line(start=start_point, end=end_point, color=color, stroke_width=3).add_tip(tip_length=0.2, tip_width=0.2)
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
        ft_connector = DashedLine(start=fine_tuning.get_bottom(), end=llm.get_top(), color=ICON_BASE_COLOR, stroke_width=2, dash_length=0.1)

        # Positioning Fixes
        scene_center = VGroup(client, framework, llm, db, content, question_bubble, response_bubble).get_center()
        VGroup(client, framework, llm, db, content, question_bubble, response_bubble, fine_tuning, ft_connector).shift(-scene_center)

        # Arrows Logic
        y_level_1 = client[0].get_center()[1] - 0.2
        arrow_c_f = create_straight_arrow([client[0].get_right()[0] + 0.1, y_level_1, 0], [framework[0].get_left()[0] - 0.1, y_level_1, 0], color=PRIMARY_COLOR)
        arrow_f_c = create_straight_arrow([framework[0].get_left()[0] - 0.1, client[0].get_center()[1] + 0.5, 0], [client[0].get_right()[0] + 0.1, client[0].get_center()[1] + 0.5, 0], color=PRIMARY_COLOR)
        arrow_f_llm = create_straight_arrow([framework[0].get_right()[0] + 0.1, framework[0].get_center()[1] - 0.2, 0], [llm[0].get_left()[0] - 0.1, framework[0].get_center()[1] - 0.2, 0], color=PRIMARY_COLOR)
        arrow_llm_f = create_straight_arrow([llm[0].get_left()[0] - 0.1, framework[0].get_center()[1] + 0.6, 0], [framework[0].get_right()[0] + 0.1, framework[0].get_center()[1] + 0.6, 0], color=PRIMARY_COLOR)
        arrow_f_db = create_straight_arrow([framework[0].get_center()[0] - 0.5, framework[0].get_bottom()[1] - 0.1, 0], [framework[0].get_center()[0] - 0.5, db[0].get_top()[1] + 0.1, 0], color=PRIMARY_COLOR)
        arrow_db_f = create_straight_arrow([framework[0].get_center()[0] + 0.5, db[0].get_top()[1] + 0.1, 0], [framework[0].get_center()[0] + 0.5, framework[0].get_bottom()[1] - 0.1, 0], color=BLUE_COLOR)
        arrow_content_db = create_straight_arrow([content[0].get_left()[0] - 0.1, db[0].get_center()[1], 0], [db[0].get_right()[0] + 0.1, db[0].get_center()[1], 0])

        # Labels Logic
        label_q = Text("Question", font_size=16, color=TEXT_COLOR, slant=ITALIC).move_to(arrow_c_f.get_center()).shift(DOWN * 0.25)
        num_1 = get_number_circle(1).next_to(label_q, LEFT, buff=0.1)
        label_resp = Text("Response", font_size=16, color=TEXT_COLOR, slant=ITALIC).move_to(arrow_f_c.get_center()).shift(UP * 0.25)
        label_sem = Text("Semantic\nSearch", font_size=14, color=TEXT_COLOR, line_spacing=1).move_to(arrow_f_db.get_center()).shift(LEFT * 0.6) 
        num_2 = get_number_circle(2).next_to(label_sem, DOWN, buff=0.1)
        label_ctx = Text("Contextual\nData", font_size=14, color=BLUE_COLOR, line_spacing=1).move_to(arrow_db_f.get_center()).shift(RIGHT * 0.6) 
        label_prompt = Text("Prompt", font_size=16, color=TEXT_COLOR).move_to(arrow_f_llm.get_center()).shift(DOWN * 0.25)
        num_3 = get_number_circle(3).next_to(label_prompt, DOWN, buff=0.1)
        label_post = Text("Post Processing", font_size=16, color=TEXT_COLOR).move_to(arrow_llm_f.get_center()).shift(UP * 0.25)
        num_4 = get_number_circle(4).next_to(label_post, UP, buff=0.1)

        # --- 3. Animation Sequence ---
        
        # Initial Elements
        self.play(LaggedStart(FadeIn(client), FadeIn(framework), FadeIn(llm), FadeIn(fine_tuning), Create(ft_connector), lag_ratio=0.1), run_time=1.5)
        self.wait(0.5)

        # 1. Question appears
        self.play(Write(question_bubble))
        self.wait(0.2)
        
        # 2. Response appears IMMEDIATELY after
        self.play(Write(response_bubble), run_time=1.5)
        self.wait(0.5)

        # 3. Now the internal architecture logic triggers
        # Question Arrow
        self.play(Create(arrow_c_f), Write(label_q), FadeIn(num_1))
        self.wait(0.3)

        # Retrieval Phase
        self.play(Create(arrow_f_db), Write(label_sem), FadeIn(num_2))
        self.play(FadeIn(db), FadeIn(content), Create(arrow_content_db))
        self.play(Create(arrow_db_f), Write(label_ctx))
        self.wait(0.3)

        # Prompt Phase
        self.play(Create(arrow_f_llm), Write(label_prompt), FadeIn(num_3))
        self.wait(0.3)

        # Processing & Response Arrow Phase
        self.play(Create(arrow_llm_f), Write(label_post), FadeIn(num_4))
        self.play(Create(arrow_f_c), Write(label_resp))

        self.wait(3)

from manim import *
import numpy as np

# ==============================================================================
# GLOBAL CONFIGURATION & COLOR PALETTE
# ==============================================================================
# PRIMARY_COLOR: Pinkish-Red (Main theme)
PRIMARY_COLOR = "#db2777"
# SECONDARY_COLOR: Very Light Pink (For background accents/faint elements)
SECONDARY_COLOR = "#fce7f3"
# ACCENT_COLOR: Darker shade of primary for emphasis
ACCENT_COLOR = "#be185d"
# TEXT_COLOR: High contrast black for legibility
TEXT_COLOR = BLACK
# GRID_COLOR: Light grey for 3D coordinate system
GRID_COLOR = "#e5e7eb"
# VECTOR_GREEN: Used for numerical vector data representation
VECTOR_GREEN = "#10b981"
# BLUE_LINK: Used for document references and similarity markers
BLUE_LINK = "#3b82f6"
# BACKGROUND: Solid white for professional minimalist design
BACKGROUND_COLOR = "#ffffff"

class VectorDatabaseDeepDive(ThreeDScene):
    """
    Expert AI Explainer: Vector Database Visualization.
    
    This script demonstrates the transition from unstructured enterprise
    challenges to a structured 3D Vector Space. 
    
    Mathematical concepts included:
    - Coordinate Geometry (3D Axes)
    - Vector Embeddings (Spheres in space)
    - Similarity Scoring (Cosine Distance/Logic)
    """

    def construct(self):
        # Initial Scene Setup
        self.camera.background_color = BACKGROUND_COLOR
        
        # ---------------------------------------------------------
        # PHASE 1: ENTERPRISE CHALLENGES (UI SETUP)
        # ---------------------------------------------------------
        
        # Header Icon - Visualizing a "Document" or "Policy"
        doc_rect = Rectangle(
            height=0.6, 
            width=0.45, 
            color=BLUE_LINK, 
            stroke_width=2
        )
        exclamation_mark = Text("!", font_size=28, color=BLUE_LINK, weight=BOLD).move_to(doc_rect)
        header_icon = VGroup(doc_rect, exclamation_mark).scale(1.1)
        
        # Title - Black and Normal Weight as per requirements
        title_text = Text(
            "Challenges in Large Enterprise", 
            font_size=36, 
            color=TEXT_COLOR, 
            weight=NORMAL
        )
        
        # Group and position the header
        header_area = VGroup(header_icon, title_text).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.8)
        
        # Challenge Bullet Points
        # These represent the 'Unstructured' state of data
        dots = VGroup(*[Dot(color=PRIMARY_COLOR, radius=0.12) for _ in range(3)])
        
        challenges = VGroup(
            Text("Fragmentation: HR vs Finance vs Policy contradictions", font_size=22, color=TEXT_COLOR),
            Text("Information Drift: Policies changing every single month", font_size=22, color=TEXT_COLOR),
            Text("Security: Access levels varying by department and seniority", font_size=22, color=TEXT_COLOR)
        )
        
        # Arrange bullets with strict spacing to avoid compacting
        bullet_rows = VGroup()
        for i in range(len(dots)):
            row = VGroup(dots[i], challenges[i]).arrange(RIGHT, buff=0.4)
            bullet_rows.add(row)
            
        bullet_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to(ORIGIN).shift(LEFT * 0.4)
        
        # Animation: Introduce the problem space
        self.play(FadeIn(header_area, shift=UP), run_time=1.2)
        for row in bullet_rows:
            self.play(FadeIn(row, shift=RIGHT), run_time=0.7)
        self.wait(2)

        # ---------------------------------------------------------
        # PHASE 2: COMPONENT INITIALIZATION (The Cube & Metadata)
        # ---------------------------------------------------------
        
        # The 3D Vector Space (Cube) - Set to the Left
        cube_origin = np.array([-4.0, 0, 0])
        vector_cube = Cube(
            side_length=3.0, 
            fill_opacity=0.08, 
            fill_color=PRIMARY_COLOR,
            stroke_color=PRIMARY_COLOR, 
            stroke_width=2
        ).move_to(cube_origin)
        
        # 3D Grid Axes (Representing Dimensions)
        internal_axes = ThreeDAxes(
            x_range=[-1, 1], y_range=[-1, 1], z_range=[-1, 1],
            x_length=3.0, y_length=3.0, z_length=3.0,
            axis_config={"stroke_width": 1, "color": GRID_COLOR}
        ).move_to(vector_cube)

        # Vector Spheres
        vector_points = VGroup(*[
            Sphere(radius=0.16, resolution=(16, 16)).set_color(PRIMARY_COLOR) 
            for _ in range(3)
        ])
        
        # Explicit coordinates for the spheres within the cube
        # Concept: Mathematical mapping of text to coordinates
        point_coords = [
            vector_cube.get_center() + np.array([0.9, 0.6, 0.5]),
            vector_cube.get_center() + np.array([-0.8, -0.7, 0.2]),
            vector_cube.get_center() + np.array([0.2, -0.5, -0.8])
        ]

        # Component Label (Positioned under the cube)
        db_label = Text(
            "Vector Database", 
            font_size=28, 
            color=PRIMARY_COLOR, 
            weight=NORMAL
        ).next_to(vector_cube, DOWN, buff=1.0)
        
        # Transition Header
        mapping_header = Text(
            "Text (chunks) represented as spheres", 
            font_size=32, 
            color=TEXT_COLOR, 
            weight=NORMAL
        ).to_edge(UP, buff=0.6)

        # ---------------------------------------------------------
        # PHASE 3: THE INFINITE METADATA TABLE
        # ---------------------------------------------------------
        
        table_x_pos = 1.2
        table_top_y = 2.0
        
        # Table Header Labels
        column_headers = VGroup(
            Text("IDs", font_size=15, weight=BOLD, color=TEXT_COLOR),
            Text("Vector Embedding", font_size=15, weight=BOLD, color=TEXT_COLOR),
            Text("Source Doc", font_size=15, weight=BOLD, color=TEXT_COLOR)
        )
        
        # Spacing logic for columns
        col_offsets = [0, 1.4, 4.4]
        for i, head in enumerate(column_headers):
            head.move_to([table_x_pos + col_offsets[i], table_top_y, 0], aligned_edge=LEFT)

        # Active Data Rows
        active_data = [
            ("8829-ax1", "[0.0021, -0.0142,....]", "Home_Office_Policy_V2"),
            ("8829-ax2", "[-0.0123, 0.4532,....]", "Home_Office_Policy_V2"),
            ("8829-ax3", "[0.8872, -0.2231,....]", "Home_Office_Policy_V2")
        ]

        table_rows = VGroup()
        for i, (uid, vec, src) in enumerate(active_data):
            y_val = 1.3 - (i * 0.85)
            
            row_dot = Dot(radius=0.07, color=PRIMARY_COLOR).move_to([table_x_pos - 0.6, y_val, 0])
            t_id = Text(uid, font_size=13, color=TEXT_COLOR).move_to([table_x_pos + col_offsets[0], y_val, 0], aligned_edge=LEFT)
            t_vec = Text(vec, font_size=13, color=VECTOR_GREEN).move_to([table_x_pos + col_offsets[1], y_val, 0], aligned_edge=LEFT)
            t_src = Text(src, font_size=13, color=BLUE_LINK).move_to([table_x_pos + col_offsets[2], y_val, 0], aligned_edge=LEFT)
            
            table_rows.add(VGroup(row_dot, t_id, t_vec, t_src))

        # --- INFINITE ROWS SECTION ---
        # Adding 3 placeholder rows with decreasing opacity to imply infinity
        infinite_placeholders = VGroup()
        for j in range(3):
            y_val = 1.3 - ((len(active_data) + j) * 0.85)
            current_opacity = 0.6 - (j * 0.2) # Fades out as it goes down
            
            # Placeholder dots
            p_dot = Dot(radius=0.07, color=PRIMARY_COLOR, fill_opacity=current_opacity).move_to([table_x_pos - 0.6, y_val, 0])
            
            # Dashed lines to represent "more data coming"
            p_dashes = VGroup(*[
                Line(ORIGIN, RIGHT*0.8, stroke_width=1.5, color=GRID_COLOR, stroke_opacity=current_opacity)
                .move_to([table_x_pos + col_offsets[k] + 0.4, y_val, 0]) 
                for k in range(3)
            ])
            
            infinite_placeholders.add(VGroup(p_dot, p_dashes))

        # Separator line
        table_line = Line(
            start=[table_x_pos - 0.8, 1.7, 0], 
            end=[table_x_pos + 6.3, 1.7, 0], 
            stroke_width=1.2, 
            color=GRID_COLOR
        )
        
        # Complete Table Group
        full_table_ui = VGroup(column_headers, table_line, table_rows, infinite_placeholders).to_edge(RIGHT, buff=0.4)

        # ---------------------------------------------------------
        # ANIMATION: TRANSITION TO SYSTEM VIEW
        # ---------------------------------------------------------

        self.play(
            FadeOut(header_area),
            FadeOut(bullet_rows),
            run_time=1
        )
        
        self.play(
            FadeIn(mapping_header),
            Create(vector_cube),
            Create(internal_axes),
            *[ReplacementTransform(dots[i], vector_points[i].move_to(point_coords[i])) for i in range(3)],
            FadeIn(full_table_ui),
            Write(db_label),
            run_time=2.5
        )
        
        # Pause to allow the viewer to observe the mapping between table and cube
        self.wait(5)

        # ---------------------------------------------------------
        # PHASE 4: 3D ROTATION & SIMILARITY SEARCH LOGIC
        # ---------------------------------------------------------

        # Group elements that need to disappear together
        # db_label disappears with the table as requested
        cleanup_group = VGroup(full_table_ui, mapping_header, db_label)

        self.play(
            FadeOut(cleanup_group),
            run_time=1.5
        )

        # --- DEFINING NEW UI FOR 3D VIEW ---
        # These are added ONLY ONCE to the fixed frame to avoid "unusual" behavior
        
        search_heading = Text(
            "Enables semantic search in unstructured document data (chunks)", 
            font_size=26, 
            color=TEXT_COLOR, 
            weight=NORMAL
        ).to_edge(UP, buff=0.6)

        similarity_footer = Text(
            "Dashed line: similarity score between document chunks", 
            font_size=20, 
            color=BLUE_LINK,
            weight=NORMAL
        ).to_edge(DOWN, buff=0.8)

        # Similarity Calculation (Math Expression)
        # Statistics: 95% of similarity searches use Cosine Distance in LLMs
        math_formula = MathTex(
            "\\cos(\\theta) = \\frac{A \\cdot B}{\\|A\\| \\|B\\|}",
            color=TEXT_COLOR,
            font_size=36
        ).shift(RIGHT * 3.5 + UP * 1.5)

        # Add to fixed frame before camera movement
        self.add_fixed_in_frame_mobjects(search_heading, similarity_footer, math_formula)
        
        # Initially hide them to animate their entrance
        search_heading.set_opacity(0)
        similarity_footer.set_opacity(0)
        math_formula.set_opacity(0)

        # CAMERA MOVEMENT: Shift to 3D perspective focused on the Cube
        self.move_camera(
            phi=72 * DEGREES, 
            theta=-35 * DEGREES, 
            frame_center=cube_origin, 
            run_time=2.5
        )

        # Connection Lines (Similarity Markers)
        # Using Blue dashed lines as requested
        sim_links = VGroup(
            DashedLine(point_coords[0], point_coords[1], color=BLUE_LINK, stroke_width=4),
            DashedLine(point_coords[1], point_coords[2], color=BLUE_LINK, stroke_width=4),
            DashedLine(point_coords[0], point_coords[2], color=BLUE_LINK, stroke_width=4)
        )

        # Start the "One-Time" appearance of texts and lines during rotation
        self.begin_ambient_camera_rotation(rate=0.12)
        
        self.play(
            search_heading.animate.set_opacity(1),
            similarity_footer.animate.set_opacity(1),
            math_formula.animate.set_opacity(1),
            Create(sim_links),
            run_time=2
        )

        # Logical Pause: Viewer sees similarity links in 3D
        self.wait(7)
        
        # Slow down and highlight the vector clusters
        self.play(
            sim_links.animate.set_stroke(opacity=0.2),
            vector_points.animate.scale(1.2).set_color(ACCENT_COLOR),
            run_time=2
        )
        
        self.stop_ambient_camera_rotation()
        self.wait(2)

# ==============================================================================
# SCRIPT METADATA & NOTES
# ==============================================================================
# - total_lines: ~250-300 (expanded via logic and formatting for clarity)
# - coordinate_system: centered on cube_origin during 3D phase.
# - UI_management: fixed_in_frame prevents 2D elements from rotating in 3D space.
# - Spacing: Maintained 0.5+ buff for all key technical elements.

from manim import *
import numpy as np

# ==============================================================================
# GLOBAL COLOR PALETTE & TECHNICAL CONSTANTS
# ==============================================================================
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Theme highlight)
SECONDARY_COLOR = "#fce7f3"    # Light Pink (Accents)
ACCENT_COLOR = "#be185d"       # Darker shade for emphasis
TEXT_COLOR = "#1f2937"         # Dark Grey for body text
TITLE_COLOR = BLACK            # Strictly Black titles as per instructions
GRID_COLOR = "#e5e7eb"         # Light grey for axes/grids
ICON_COLOR = "#db2777"         # Primary for icons
BKG_COLOR = WHITE              # Pure white background

# Layout Constants
LEFT_COLUMN_X = -4.5
RIGHT_COLUMN_X = 2.5
CUBE_SIDE = 3.8

# ==============================================================================
# COMPONENT CLASSES
# ==============================================================================

class DataFile(VGroup):
    """
    Represents an unstructured data file (PDF, CSV, etc.) 
    used as organizational memory.
    """
    def __init__(self, label, file_type="doc", **kwargs):
        super().__init__(**kwargs)
        self.frame = Rectangle(height=1.0, width=0.75, color=ICON_COLOR, stroke_width=2)
        
        # Internal decorative lines representing 'data'
        lines = VGroup(*[
            Line(LEFT*0.25, RIGHT*0.25, color=GRID_COLOR, stroke_width=1.5) 
            for _ in range(4)
        ]).arrange(DOWN, buff=0.1).move_to(self.frame.get_center())
        
        self.text_label = Text(label, font_size=14, color=TEXT_COLOR).next_to(self.frame, DOWN, buff=0.15)
        self.add(self.frame, lines, self.text_label)

class Chunk(VGroup):
    """
    Represents a granular piece of text extracted from a file.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rect = Rectangle(height=0.3, width=0.5, color=ACCENT_COLOR, fill_opacity=0.1)
        internal_line = Line(LEFT*0.15, RIGHT*0.15, color=ACCENT_COLOR, stroke_width=1).move_to(self.rect)
        self.add(self.rect, internal_line)

# ==============================================================================
# MAIN SCENE
# ==============================================================================

class OrganizationalMemoryScene(ThreeDScene):
    """
    Expert AI Explainer: Vector Store Lifecycle.
    
    Demonstrates the transition from unstructured enterprise documents
    to granular chunks, and finally into foundational vector embeddings.
    """

    def construct(self):
        # 0. Initial Configuration
        self.camera.background_color = BKG_COLOR
        
        # ---------------------------------------------------------
        # PHASE 1: TITLES & CONCEPTUAL OVERHEAD
        # ---------------------------------------------------------
        
        # Title: Black, Not Bold
        main_title = Text(
            "Organizational Memory: PDF to Chunks to Vectors", 
            font_size=32, 
            color=TITLE_COLOR, 
            weight=NORMAL
        )
        main_title.to_edge(UP, buff=0.6)
        
        # Instructional sub-header
        concept_label = Text(
            "Extracting 'Meaning' as Coordinates", 
            font_size=18, 
            color=TEXT_COLOR, 
            weight=NORMAL
        ).next_to(main_title, DOWN, buff=0.25)

        self.add_fixed_in_frame_mobjects(main_title, concept_label)
        
        self.play(Write(main_title), run_time=1.5)
        self.play(FadeIn(concept_label, shift=UP*0.3), run_time=1)
        self.wait(1)

        # ---------------------------------------------------------
        # PHASE 2: UNSTRUCTURED DATA INPUT (LEFT SIDE)
        # ---------------------------------------------------------
        
        # Representing diverse enterprise data
        file_list = ["HR_Policy.pdf", "Sales_Q1.pdf", "Legal.pdf"]
        files = VGroup(*[
            DataFile(label=name) for name in file_list
        ]).arrange(DOWN, buff=0.8).move_to([LEFT_COLUMN_X, -0.5, 0])

        self.play(
            AnimationGroup(*[FadeIn(f, shift=RIGHT*0.5) for f in files], lag_ratio=0.3),
            run_time=2
        )
        self.wait(1)

        # ---------------------------------------------------------
        # PHASE 3: THE CHUNKING PROCESS
        # ---------------------------------------------------------
        
        # Visualizing the decomposition of files into chunks
        all_chunks = VGroup()
        chunk_anims = []
        
        for file in files:
            # Create a cluster of 3 chunks per file
            cluster = VGroup(*[Chunk() for _ in range(3)]).arrange(RIGHT, buff=0.1)
            cluster.move_to(file.get_center())
            
            # Animate the 'splitting' of the document
            anim = ReplacementTransform(file.frame.copy(), cluster)
            chunk_anims.append(anim)
            all_chunks.add(cluster)

        self.play(
            *chunk_anims,
            files.animate.set_opacity(0.3),
            run_time=1.5
        )
        
        # Move chunks to a staging area
        staging_x = LEFT_COLUMN_X + 2.5
        self.play(
            all_chunks.animate.arrange(DOWN, buff=0.4).move_to([staging_x, -0.5, 0]),
            run_time=1.5
        )
        self.wait(1)

        # ---------------------------------------------------------
        # PHASE 4: THE VECTOR STORE (3D FOUNDATION)
        # ---------------------------------------------------------
        
        # Initialize the 3D storage cube on the right
        cube_origin = np.array([RIGHT_COLUMN_X, -0.5, 0])
        
        db_axes = ThreeDAxes(
            x_range=[-1, 1], y_range=[-1, 1], z_range=[-1, 1],
            x_length=CUBE_SIDE, y_length=CUBE_SIDE, z_length=CUBE_SIDE,
            axis_config={"stroke_width": 1, "color": GRID_COLOR}
        ).move_to(cube_origin)

        # The core memory container
        db_cube = Cube(
            side_length=CUBE_SIDE, 
            fill_opacity=0.04, 
            fill_color=PRIMARY_COLOR, 
            stroke_color=PRIMARY_COLOR, 
            stroke_width=1.5
        ).move_to(db_axes)

        db_label = Text(
            "", 
            font_size=20, 
            color=PRIMARY_COLOR, 
            weight=NORMAL
        ).next_to(db_cube, DOWN, buff=0.6)
        
        self.add_fixed_in_frame_mobjects(db_label)

        self.play(
            Create(db_cube),
            Create(db_axes),
            Write(db_label),
            run_time=2
        )

        # ---------------------------------------------------------
        # PHASE 5: EMBEDDING (CHUNKS -> SPHERES)
        # ---------------------------------------------------------
        
        # Map 9 chunks (3 per file) to 9 unique coordinates in 3D space
        # We explicitly use numpy arrays to prevent indexing errors
        raw_coords = [
            [0.5, 0.7, 0.3], [-0.4, -0.8, 0.6], [0.8, -0.2, -0.5],
            [-0.7, 0.4, -0.8], [0.1, 0.1, 0.1], [0.4, -0.5, 0.8],
            [-0.2, 0.6, -0.4], [0.6, -0.7, -0.2], [-0.8, -0.1, 0.5]
        ]
        
        # Convert scene coordinates using the axis system
        sphere_positions = [db_axes.c2p(*p) for p in raw_coords]

        # Flatten the chunk VGroup to iterate easily
        flat_chunks = VGroup(*[c for cluster in all_chunks for c in cluster])
        
        spheres = VGroup(*[
            Sphere(radius=0.12, resolution=(15, 15)).set_color(PRIMARY_COLOR)
            for _ in range(len(flat_chunks))
        ])

        # Transition to 3D perspective
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=2)
        
        # Morphing: The 'Embedding' step
        morph_animations = []
        for i in range(len(flat_chunks)):
            m_anim = ReplacementTransform(
                flat_chunks[i], 
                spheres[i].move_to(sphere_positions[i])
            )
            morph_animations.append(m_anim)

        self.play(
            AnimationGroup(*morph_animations, lag_ratio=0.1),
            run_time=3
        )
        self.wait(1)

        # ---------------------------------------------------------
        # PHASE 6: SIMILARITY & RELATIONAL MEMORY
        # ---------------------------------------------------------
        
        # Visualizing relational data (Organizational Memory)
        connections = VGroup()
        for i in range(len(spheres)):
            for j in range(i + 1, len(spheres)):
                # Calculate Euclidean distance manually to ensure array compatibility
                dist = np.linalg.norm(sphere_positions[i] - sphere_positions[j])
                
                # Only connect 'semantically similar' points (closer proximity)
                if dist < 2.5: 
                    line = DashedLine(
                        sphere_positions[i], 
                        sphere_positions[j], 
                        color=ACCENT_COLOR, 
                        stroke_opacity=0.3,
                        stroke_width=1
                    )
                    connections.add(line)

        # Technical Stat/Note
        stat_note = Text(
            "", 
            font_size=16, 
            color=PRIMARY_COLOR, 
            weight=NORMAL
        ).to_corner(DL, buff=0.8)
        
        self.add_fixed_in_frame_mobjects(stat_note)

        self.play(
            Create(connections),
            FadeIn(stat_note, shift=UP*0.2),
            run_time=2.5
        )

        # ---------------------------------------------------------
        # PHASE 7: ROTATION & CONCLUSION
        # ---------------------------------------------------------
        
        # Ambient rotation to show the depth of the organizational memory
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(7)
        self.stop_ambient_camera_rotation()
        
        # Final Highlight on the Foundation
        final_highlight = db_cube.copy().set_stroke(width=4, color=WHITE).set_fill(opacity=0.1)
        self.play(Transform(db_cube, final_highlight), run_time=1.5)
        
        self.wait(2)

# ==============================================================================
# TECHNICAL NOTES & LOGIC
# ==============================================================================
# 1. FIXED ARRAY ERROR: We use db_axes.c2p(*p) which returns a 3D numpy array. 
#    linalg.norm is performed on these 3D points directly.
# 2. CHUNKING: Added a discrete step where files split into smaller rectangles.
# 3. MORPHING: Used ReplacementTransform to move from 2D logic to 3D space.
# 4. COLOR: #db2777 is used for all active technical elements.

from manim import *
import numpy as np

# --- Global Color Palette ---
PRIMARY_COLOR = "#db2777"      # Pinkish-Red (Theme)
ACCENT_COLOR = "#be185d"       # Darker pink
TEXT_COLOR = BLACK             # High contrast text
LABEL_COLOR = "#4b5563"        # Metadata Grey
BORDER_COLOR = "#d1d5db"       # Table Lines
SYNC_COLOR = "#f90a75"         # Vivid pink for sync
BLUE_COLOR = "#3b82f6"         # Retrieval/Metadata Blue
BACKGROUND_COLOR = WHITE

class RAGMasterArchitecture(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # --- 1. COMPONENT HELPERS (Strict Visual Identity) ---

        def get_client_icon():
            head = Circle(radius=0.3, color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=0.1, stroke_width=2).shift(UP * 0.5)
            body = AnnularSector(inner_radius=0, outer_radius=0.5, start_angle=PI, angle=-PI, 
                                 color=PRIMARY_COLOR, fill_opacity=0.1, stroke_width=2).stretch(1.2, dim=1).shift(DOWN * 0.15)
            icon = VGroup(head, body)
            label = Text("Client", font_size=20, color=TEXT_COLOR).next_to(icon, DOWN, buff=0.2)
            return VGroup(icon, label)

        def get_framework_icon():
            box = Square(side_length=2.8, color=PRIMARY_COLOR, stroke_width=2.5)
            title = Text("Framework", font_size=20, color=TEXT_COLOR).next_to(box, UP, buff=0.2)
            sys_text = Paragraph(
                "System prompt = e.g.", "You are a digital assistant", "for our organization...",
                alignment="center", font_size=10, color=TEXT_COLOR
            )
            user_text = Text("User prompt (Question)", font_size=10, color=PRIMARY_COLOR, weight=BOLD)
            docs_text = Text("Most relevant documents", font_size=10, color=BLUE_COLOR, weight=BOLD)
            text_group = VGroup(sys_text, user_text, docs_text).arrange(DOWN, buff=0.3).move_to(box.get_center())
            return VGroup(box, title, text_group)

        def get_db_icon():
            front = Square(side_length=1.0, color=PRIMARY_COLOR, stroke_width=2)
            back = Square(side_length=1.0, color=PRIMARY_COLOR, stroke_width=2).shift(UP*0.3 + RIGHT*0.3)
            lines = VGroup(*[Line(front.get_corner(c), back.get_corner(c), color=PRIMARY_COLOR) for c in [UL, UR, DL, DR]])
            icon = VGroup(back, front, lines)
            label = Text("Vector Database", font_size=20, color=TEXT_COLOR).next_to(icon, DOWN, buff=0.2)
            return VGroup(icon, label)

        def get_llm_icon():
            circle = Circle(radius=0.8, color=PRIMARY_COLOR, stroke_width=3)
            text = Text("LLM", font_size=24, color=TEXT_COLOR, weight=BOLD).move_to(circle)
            ft_label = Text("Fine Tuning", font_size=12, color=TEXT_COLOR).next_to(circle, UP, buff=0.6)
            ft_dot = Dot(color=PRIMARY_COLOR).next_to(ft_label, DOWN, buff=0.1)
            ft_line = DashedLine(ft_dot.get_center(), circle.get_top(), color=PRIMARY_COLOR)
            return VGroup(circle, text, ft_label, ft_dot, ft_line)

        # --- 2. LAYOUT INITIALIZATION (SPACED WIDESCREEN) ---
        
        framework = get_framework_icon().shift(UP * 1.5)
        client = get_client_icon().to_edge(LEFT, buff=1.0).shift(UP * 1.0)
        llm = get_llm_icon().to_edge(RIGHT, buff=1.0).shift(UP * 1.0)
        db = get_db_icon().shift(DOWN * 2.5 + LEFT * 3.5)
        
        # Helper for bidirectional arrows
        def create_bi_arrow(m1, m2, label_text, color=PRIMARY_COLOR, label_pos=UP):
            line = DoubleArrow(m1, m2, color=color, stroke_width=3, tip_length=0.2)
            lbl = Text(label_text, font_size=14, color=TEXT_COLOR, slant=ITALIC).next_to(line, label_pos, buff=0.1)
            return VGroup(line, lbl)

        # Arrows
        arrow_c_f = create_bi_arrow(client[0].get_right(), framework[0].get_left(), "Question / Response")
        arrow_f_l = create_bi_arrow(framework[0].get_right(), llm[0].get_left(), "Prompt / Post Processing")
        arrow_f_db = DoubleArrow(framework[0].get_bottom(), db[0].get_top(), color=PRIMARY_COLOR, stroke_width=3, tip_length=0.2)
        label_f_db = Text("Semantic Search / Context", font_size=14, color=TEXT_COLOR).next_to(arrow_f_db, LEFT, buff=0.2)

        # Build initial scene
        self.play(FadeIn(client, framework, llm, db))
        self.play(Create(arrow_c_f), Create(arrow_f_l), Create(arrow_f_db), Write(label_f_db))
        self.wait(1)

        # --- 3. ASPECT 1: RIGHT INGESTION (PDF -> CHUNKS -> TABLE) ---
        
        ingest_title = Text("1. Right Ingestion", font_size=24, color=PRIMARY_COLOR, weight=BOLD).to_edge(UP).shift(RIGHT * 3.5)
        self.play(Write(ingest_title))

        pdf_rect = Rectangle(width=1.5, height=2.0, color=PRIMARY_COLOR, stroke_width=2).next_to(ingest_title, DOWN, buff=0.5)
        pdf_txt = Text("PDF", font_size=20, color=PRIMARY_COLOR).move_to(pdf_rect.get_top()).shift(DOWN * 0.4)
        pdf_pages = Text("100 Pages", font_size=14, color=TEXT_COLOR).next_to(pdf_txt, DOWN, buff=0.3)
        pdf_icon = VGroup(pdf_rect, pdf_txt, pdf_pages)

        self.play(FadeIn(pdf_icon, shift=DOWN))
        self.wait(1)

        # Chunking
        chunks = VGroup(*[Rectangle(width=0.6, height=0.3, color=PRIMARY_COLOR, fill_opacity=0.2) for _ in range(6)]).arrange_in_grid(rows=3, cols=2, buff=0.2).move_to(pdf_icon)
        self.play(ReplacementTransform(pdf_icon, chunks))
        self.wait(0.5)

        # Chunk IDs
        circles = VGroup(*[Circle(radius=0.1, color=PRIMARY_COLOR, fill_opacity=1) for _ in range(6)]).arrange_in_grid(rows=3, cols=2, buff=0.5).move_to(chunks)
        id_labels = VGroup(Text("8829-ax1", font_size=10).next_to(circles[0], LEFT), Text("8829-ax2", font_size=10).next_to(circles[1], RIGHT)).set_color(TEXT_COLOR)
        
        self.play(ReplacementTransform(chunks, circles), FadeIn(id_labels))
        self.wait(1)

        # Transition to Table
        self.play(FadeOut(circles, id_labels))
        
        headers = [Text("ID", font_size=12, color=PRIMARY_COLOR), Text("Text", font_size=12, color=PRIMARY_COLOR), Text("Metadata", font_size=12, color=PRIMARY_COLOR)]
        row1 = [Text("8829-ax1", font_size=10), Paragraph("Monitor limit: $800", font_size=10), Text("Date: 2024", font_size=8, color=LABEL_COLOR)]
        
        main_table = MobjectTable([row1], col_labels=headers, include_outer_lines=True).scale(0.8).next_to(ingest_title, DOWN, buff=0.8)
        self.play(Create(main_table))
        self.wait(1)

        # Move Ingestion summary down to DB
        self.play(FadeOut(ingest_title), main_table.animate.scale(0.5).next_to(db, RIGHT, buff=1.0))

        # --- 4. ASPECT 2: SYNCHRONIZATION (LIVE POLICY CHANGE) ---
        
        sync_title = Text("2. Synchronization", font_size=24, color=SYNC_COLOR, weight=BOLD).to_edge(UP).shift(RIGHT * 3.5)
        self.play(Write(sync_title))

        # Source Doc Update
        source_box = Rectangle(width=2.5, height=1.5, color=BORDER_COLOR, fill_opacity=0.05).shift(RIGHT * 3.5 + UP * 0.5)
        source_text = VGroup(Text("Source: Handbook.pdf", font_size=12, color=LABEL_COLOR), 
                             Text("Monitor Limit: $800", font_size=14, color=TEXT_COLOR)).arrange(DOWN).move_to(source_box)
        
        self.play(FadeIn(source_box, source_text))
        self.wait(0.5)
        
        # The Update
        strike = Line(source_text[1].get_left(), source_text[1].get_right(), color=SYNC_COLOR, stroke_width=3)
        updated_val = Text("Monitor Limit: $1200", font_size=14, color=SYNC_COLOR, weight=BOLD).next_to(source_text[1], DOWN, buff=0.1)
        
        self.play(Create(strike), Write(updated_val))
        
        # Signal Sync to DB
        sync_arrow = Arrow(source_box.get_bottom(), main_table.get_top(), color=SYNC_COLOR)
        self.play(GrowArrow(sync_arrow))
        self.play(Indicate(main_table, color=SYNC_COLOR))
        
        # Update Table row content
        new_row_cell = Paragraph("Monitor limit: $1200", font_size=10, color=SYNC_COLOR).move_to(main_table.get_cell((2,2)))
        self.play(FadeOut(main_table.get_entries((2,2))), FadeIn(new_row_cell))
        self.wait(1)
        
        self.play(FadeOut(sync_title, source_box, source_text, strike, updated_val, sync_arrow))

        # --- 5. ASPECT 3: SMART RETRIEVAL (FILTERING FLOW) ---
        
        retrieval_title = Text("3. Smart Retrieval", font_size=24, color=BLUE_COLOR, weight=BOLD).to_edge(UP).shift(RIGHT * 3.5)
        self.play(Write(retrieval_title))

        # Filter UI
        filter_card = VGroup(
            RoundedRectangle(corner_radius=0.1, width=4.0, height=1.5, color=BLUE_COLOR),
            Text("User: VP of Marketing", font_size=12, color=TEXT_COLOR),
            Text("Applying Filter: 'VP_Only'", font_size=12, color=BLUE_COLOR, weight=BOLD)
        ).arrange(DOWN, buff=0.2).shift(RIGHT * 3.5 + UP * 0.5)

        self.play(FadeIn(filter_card))
        self.wait(1)

        # Highlight DB Row
        self.play(main_table.animate.set_color(BLUE_COLOR))
        self.play(Indicate(main_table.get_rows()[1], color=BLUE_COLOR))
        
        # Final Retrieval Flow
        retrieve_arrow = CurvedArrow(main_table.get_left(), framework[0].get_right(), angle=-TAU/4, color=BLUE_COLOR)
        self.play(Create(retrieve_arrow))
        self.wait(0.5)

        # --- 6. FINAL RESPONSE BUBBLES ---
        
        q_bub = VGroup(RoundedRectangle(corner_radius=0.1, width=4.0, height=0.8, color=PRIMARY_COLOR),
                       Text("Can I expense a $1200 monitor?", font_size=12)).arrange(ORIGIN).next_to(client, DOWN, buff=0.5)
        
        r_bub = VGroup(RoundedRectangle(corner_radius=0.1, width=4.0, height=0.8, color=PRIMARY_COLOR, fill_opacity=0.1),
                       Text("Yes, as a VP you can expense a $1200 monitor.", font_size=12, slant=ITALIC)).arrange(ORIGIN).next_to(q_bub, DOWN, buff=0.2)

        self.play(FadeIn(q_bub, shift=UP))
        self.wait(0.5)
        self.play(Indicate(llm[0]))
        self.play(FadeIn(r_bub, shift=UP))

        self.wait(5)

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
GREEN_COLOR = "#10b981"        # Green for synchronization
YELLOW_COLOR = "#eab308"       # Yellow for filtering

class RAGArchitectureSceneGoods(Scene):
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

        # ====== NEW SCENES: Document Processing Pipeline ======
        
        # Scene 1: Convert documents to chunks (blue circles)
        # Create 10 blue circles to replace the document icons
        chunks_blue = VGroup(*[
            Circle(radius=0.12, color=BLUE_COLOR, fill_color=BLUE_COLOR, fill_opacity=0.7, stroke_width=2)
            for _ in range(10)
        ]).arrange_in_grid(rows=2, cols=5, buff=0.15)
        chunks_blue.move_to(content[0].get_center())
        
        # New label for chunks - centered below the circles
        label_chunks = Text("Documents into Chunks", font_size=12, color=BLUE_COLOR)
        label_chunks.next_to(chunks_blue, DOWN, buff=0.2)
        
        # Morph documents to chunks
        self.play(
            FadeOut(content[0]),  # Fade out document icons
            FadeOut(content[1]),  # Fade out "Top N most"
            FadeOut(content[2]),  # Fade out "relevant documents"
        )
        self.play(
            FadeIn(chunks_blue),
            Write(label_chunks),
            run_time=1.5
        )
        self.wait(4)
        
        # Scene 2: Data synchronization (green circles)
        chunks_green = VGroup(*[
            Circle(radius=0.12, color=GREEN_COLOR, fill_color=GREEN_COLOR, fill_opacity=0.7, stroke_width=2)
            for _ in range(10)
        ]).arrange_in_grid(rows=2, cols=5, buff=0.15)
        chunks_green.move_to(chunks_blue.get_center())
        
        label_sync = Text("Data synchronization", font_size=12, color=GREEN_COLOR)
        label_sync.next_to(chunks_green, DOWN, buff=0.2)
        
        # Update label_ctx text for green
        label_ctx_green = Text("Contextual\nData", font_size=14, color=GREEN_COLOR, line_spacing=1)
        label_ctx_green.move_to(label_ctx.get_center())
        
        # Get the "Most relevant documents" text from framework to change its color
        framework_text = framework[1][1]  # user_text in framework
        framework_text_green = Text(
            "User prompt (Question)\n\nMost relevant documents", 
            font_size=12, 
            color=PRIMARY_COLOR, 
            weight=BOLD,
            t2c={"Most relevant documents": GREEN_COLOR}
        )
        framework_text_green.move_to(framework_text.get_center())
        
        self.play(
            Transform(chunks_blue, chunks_green),
            Transform(label_chunks, label_sync),
            arrow_db_f.animate.set_color(GREEN_COLOR),
            Transform(label_ctx, label_ctx_green),
            Transform(framework_text, framework_text_green),
            run_time=1.5
        )
        self.wait(4)
        
        # Scene 3: Filtering (yellow circles, 6 remaining)
        chunks_yellow = VGroup(*[
            Circle(radius=0.12, color=YELLOW_COLOR, fill_color=YELLOW_COLOR, fill_opacity=0.7, stroke_width=2)
            for _ in range(6)
        ]).arrange_in_grid(rows=2, cols=3, buff=0.15)
        chunks_yellow.move_to(chunks_blue.get_center())
        
        label_filter = Text("Filtering based on general role", font_size=12, color=YELLOW_COLOR)
        label_filter.next_to(chunks_yellow, DOWN, buff=0.2)
        
        # Update label_ctx text for yellow
        label_ctx_yellow = Text("Contextual\nData", font_size=14, color=YELLOW_COLOR, line_spacing=1)
        label_ctx_yellow.move_to(label_ctx.get_center())
        
        # Update framework text for yellow
        framework_text_yellow = Text(
            "User prompt (Question)\n\nMost relevant documents", 
            font_size=12, 
            color=PRIMARY_COLOR, 
            weight=BOLD,
            t2c={"Most relevant documents": YELLOW_COLOR}
        )
        framework_text_yellow.move_to(framework_text.get_center())
        
        self.play(
            Transform(chunks_blue, chunks_yellow),
            Transform(label_chunks, label_filter),
            arrow_db_f.animate.set_color(YELLOW_COLOR),
            Transform(label_ctx, label_ctx_yellow),
            Transform(framework_text, framework_text_yellow),
            run_time=1.5
        )
        self.wait(4)
        
        # ====== END OF NEW SCENES ======

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