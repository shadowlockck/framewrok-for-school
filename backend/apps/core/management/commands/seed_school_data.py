from django.core.management.base import BaseCommand
from datetime import date, time
from apps.core.models import SchoolProfile, ThemeSettings
from apps.legal.models import LegalDocumentCategory, LegalDocument, FinancialReport, StaffMember, Vacancy
from apps.admissions.models import ServiceTerritory, ClassCapacity, EnrolledStudent, AdmissionLottery
from apps.nutrition.models import CateringProvider, DailyMenu
from apps.safety.models import AntiBullyingPolicy
from apps.news.models import NewsCategory, NewsArticle
from apps.schedule.models import BellSchedule, LessonSchedule
from apps.gallery.models import PhotoAlbum, GalleryPhoto

class Command(BaseCommand):
    help = 'Наповнення бази даних зразковими даними типового закладу загальної середньої освіти'

    def handle(self, *args, **options):
        self.stdout.write('Початок генерації зразкових даних школи...')

        # 1. School Profile
        school, created = SchoolProfile.objects.get_or_create(
            edrpou='12345678',
            defaults={
                'name': 'Ліцей «Інтелект та Інновації» Київської міської ради',
                'short_name': 'Ліцей «Інтелект та Інновації»',
                'founder': 'Київська міська рада (орган місцевого самоврядування від імені територіальної громади)',
                'address': '01001, м. Київ, вул. Освітня, 15',
                'phone': '+38 (044) 123-45-67',
                'email': 'school@osvita.kyiv.ua',
                'website': 'https://intellect-school.kyiv.ua',
                'licensed_capacity': 900,
                'actual_students': 824,
                'education_language': 'Українська',
            }
        )

        # 2. Theme
        ThemeSettings.objects.get_or_create(
            school=school,
            defaults={
                'primary_color': '#1e3a8a',
                'primary_hover': '#172554',
                'secondary_color': '#059669',
                'accent_color': '#d97706',
                'font_family': 'Inter, system-ui, sans-serif'
            }
        )

        # 3. Legal Categories & Documents
        cat_constituent, _ = LegalDocumentCategory.objects.get_or_create(name='Установчі документи', defaults={'order': 1})
        cat_license, _ = LegalDocumentCategory.objects.get_or_create(name='Ліцензування та акредитація', defaults={'order': 2})
        cat_structure, _ = LegalDocumentCategory.objects.get_or_create(name='Управління та структура', defaults={'order': 3})
        cat_edu, _ = LegalDocumentCategory.objects.get_or_create(name='Освітні програми', defaults={'order': 4})
        cat_reports, _ = LegalDocumentCategory.objects.get_or_create(name='Якість освіти та звіти', defaults={'order': 5})

        LegalDocument.objects.get_or_create(
            title='Статут закладу загальної середньої освіти',
            defaults={
                'category': cat_constituent,
                'law_reference': 'ст. 30 ч. 2 ЗУ «Про освіту»',
                'description': 'Затверджений рішенням сесії Київської міської ради. Визначає мету, завдання, структуру та статус закладу.',
                'approval_date': date(2026, 1, 12),
                'is_active': True,
            }
        )

        LegalDocument.objects.get_or_create(
            title='Ліцензія на провадження освітньої діяльності',
            defaults={
                'category': cat_license,
                'law_reference': 'ст. 30 ч. 2 ЗУ «Про освіту»',
                'description': 'Рівні: початкова, базова та профільна середня освіта. Видана Департаментом освіти і науки. Безстрокова.',
                'approval_date': date(2023, 9, 5),
                'is_active': True,
            }
        )

        LegalDocument.objects.get_or_create(
            title='Освітня програма та перелік навчальних компонентів',
            defaults={
                'category': cat_edu,
                'law_reference': 'ст. 30 ч. 2 ЗУ «Про освіту»',
                'description': 'Навчальний план, опис модельних навчальних програм НУШ, форма оцінювання результатів навчання здобувачів.',
                'approval_date': date(2026, 8, 28),
                'is_active': True,
            }
        )

        # 4. Financial Reports (п. 3 ст. 30)
        FinancialReport.objects.get_or_create(
            title='Кошторис закладу освіти на 2026 рік (зі змінами)',
            defaults={
                'report_type': 'estimate',
                'period': '2026 рік',
                'total_amount': 14250000.00,
                'approval_date': date(2026, 9, 15),
                'publish_date': date(2026, 9, 22),
                'file': 'legal/finance/estimate_2026.pdf',
                'notes': 'Затверджено розпорядником публічних коштів. Оприлюднено в межах 10 робочих днів.'
            }
        )

        FinancialReport.objects.get_or_create(
            title='Звіт про надходження та використання коштів загального фонду (Форма №2)',
            defaults={
                'report_type': 'quarterly_report',
                'period': 'III квартал 2026',
                'total_amount': 10890400.00,
                'approval_date': date(2026, 10, 5),
                'publish_date': date(2026, 10, 12),
                'file': 'legal/finance/report_q3_2026.pdf',
                'notes': 'Фактичне фінансування захищених статей: заробітна плата, комунальні послуги, харчування.'
            }
        )

        # 5. Staff
        StaffMember.objects.get_or_create(
            full_name='Коваленко Олена Василівна',
            defaults={
                'position': 'Директор ліцею, вчитель математики',
                'is_administration': True,
                'category': 'Вища категорія',
                'pedagogical_title': 'Вчитель-методист',
                'education': 'НПУ ім. М.П. Драгоманова, математичний факультет',
                'last_qualification_update': 2025,
                'order': 1,
            }
        )

        StaffMember.objects.get_or_create(
            full_name='Мельник Андрій Сергійович',
            defaults={
                'position': 'Заступник директора з навчально-виховної роботи',
                'is_administration': True,
                'category': 'Вища категорія',
                'pedagogical_title': 'Старший вчитель',
                'education': 'КНУ ім. Тараса Шевченка, фізичний факультет',
                'last_qualification_update': 2026,
                'order': 2,
            }
        )

        # 6. Territory & Classes
        ServiceTerritory.objects.get_or_create(
            street_name='вул. Освітня',
            defaults={
                'building_numbers': 'парні 2-24, непарні 1-31',
                'district': 'Шевченківський',
                'decision_doc': 'Розпорядження РДА № 142 від 15.02.2026'
            }
        )

        ServiceTerritory.objects.get_or_create(
            street_name='просп. Науки',
            defaults={
                'building_numbers': 'буд. 42, 44, 46, 48/1',
                'district': 'Шевченківський',
                'decision_doc': 'Розпорядження РДА № 142 від 15.02.2026'
            }
        )

        cls_1a, _ = ClassCapacity.objects.get_or_create(
            grade_name='1-А',
            defaults={'total_capacity': 30, 'enrolled_count': 30}
        )
        cls_1b, _ = ClassCapacity.objects.get_or_create(
            grade_name='1-Б',
            defaults={'total_capacity': 30, 'enrolled_count': 28}
        )

        # Enrolled students (LAST NAMES ONLY!)
        EnrolledStudent.objects.get_or_create(
            last_name='Бойко',
            grade=cls_1b,
            defaults={'enrollment_date': date(2026, 6, 1), 'order_number': '№ 45-У'}
        )
        EnrolledStudent.objects.get_or_create(
            last_name='Гриценко',
            grade=cls_1b,
            defaults={'enrollment_date': date(2026, 6, 1), 'order_number': '№ 45-У'}
        )

        # 7. Catering
        catering, _ = CateringProvider.objects.get_or_create(
            company_name='ТОВ «Якісне Шкільне Харчування»',
            defaults={
                'edrpou': '87654321',
                'contract_number': 'Договір № 12/26 від 10.01.2026',
                'contact_person': 'Іванова Марія Петрівна, головний технолог',
                'phone': '+38 (044) 987-65-43',
            }
        )

        # 8. Anti-Bullying Policy
        AntiBullyingPolicy.objects.get_or_create(
            title='Політика запобігання та протидії булінгу в закладі освіти',
            academic_year='2026/2027',
            defaults={
                'behavior_rules_doc': 'safety/rules/rules_2026.pdf',
                'application_procedure_doc': 'safety/procedures/application_order.pdf',
                'reaction_procedure_doc': 'safety/procedures/reaction_order.pdf',
                'action_plan_doc': 'safety/plans/action_plan_2026.pdf',
                'is_active': True,
            }
        )

        # 9. News
        cat_events, _ = NewsCategory.objects.get_or_create(name='Події та свята', defaults={'slug': 'events'})
        cat_announcements, _ = NewsCategory.objects.get_or_create(name='Оголошення', defaults={'slug': 'announcements'})

        NewsArticle.objects.get_or_create(
            title='Початок прийому заяв до 1-х класів на 2026/2027 навчальний рік',
            defaults={
                'category': cat_announcements,
                'summary': 'З 1 квітня розпочинається прийом заяв для дітей, які проживають на закріпленій території обслуговування.',
                'content': 'Подання документів можливе особисто, поштою або через електронний сервіс АІКОМ.',
                'is_urgent': True,
                'is_published': True,
            }
        )

        NewsArticle.objects.get_or_create(
            title='Перемога учнів ліцею на Всеукраїнській олімпіаді з інформатики',
            defaults={
                'category': cat_events,
                'summary': 'Команда учнів 10-х класів здобула дипломи І та ІІ ступенів.',
                'content': 'Вітаємо переможців та їхніх наставників! Пишаємося інтелектуальними здобутками ліцеїстів.',
                'is_urgent': False,
                'is_published': True,
            }
        )

        # 10. Bell Schedule
        bells = [
            (1, time(8, 30), time(9, 15), 15),
            (2, time(9, 30), time(10, 15), 20),
            (3, time(10, 35), time(11, 20), 20),
            (4, time(11, 40), time(12, 25), 15),
            (5, time(12, 40), time(13, 25), 10),
            (6, time(13, 35), time(14, 20), 10),
            (7, time(14, 30), time(15, 15), 0),
        ]
        for num, start, end, break_len in bells:
            BellSchedule.objects.get_or_create(
                lesson_number=num,
                defaults={'start_time': start, 'end_time': end, 'break_duration': break_len}
            )

        # 11. Lesson Schedule (Sample for 1-Б)
        monday_lessons = [
            (1, 'Математика', 'каб. 102', 'Коваленко О.В.'),
            (2, 'Українська мова', 'каб. 102', 'Ткаченко І.М.'),
            (3, 'Я досліджую світ', 'каб. 102', 'Ткаченко І.М.'),
            (4, 'Фізична культура', 'спортзал №1', 'Сидоренко П.В.'),
        ]
        for lesson_num, subj, room, teacher in monday_lessons:
            LessonSchedule.objects.get_or_create(
                grade=cls_1b,
                day_of_week=1,
                lesson_number=lesson_num,
                defaults={'subject': subj, 'classroom': room, 'teacher_name': teacher}
            )

        # 12. Gallery
        album, _ = PhotoAlbum.objects.get_or_create(
            title='Свято Першого дзвоника та посвята першокласників у НУШ',
            defaults={
                'description': 'Урочиста лінійка, інтерактивний квест та перший урок єдності для першокласників.',
                'event_date': date(2026, 9, 1),
            }
        )
        GalleryPhoto.objects.get_or_create(
            album=album,
            order=1,
            defaults={'caption': 'Урочисте відкриття навчального року'}
        )
        GalleryPhoto.objects.get_or_create(
            album=album,
            order=2,
            defaults={'caption': 'Першокласники у просторі Нової Української Школи'}
        )

        self.stdout.write(self.style.SUCCESS('Базу даних успішно наповнено типовими зразковими даними!'))
