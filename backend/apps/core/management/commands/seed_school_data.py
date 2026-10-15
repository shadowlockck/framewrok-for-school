from django.core.management.base import BaseCommand
from datetime import date
from apps.core.models import SchoolProfile, ThemeSettings
from apps.legal.models import LegalDocumentCategory, LegalDocument, FinancialReport, StaffMember, Vacancy
from apps.admissions.models import ServiceTerritory, ClassCapacity, EnrolledStudent, AdmissionLottery
from apps.nutrition.models import CateringProvider, DailyMenu
from apps.safety.models import AntiBullyingPolicy

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

        DailyMenu.objects.get_or_create(
            menu_date=date.today(),
            age_group='1_4',
            defaults={
                'breakfast': 'Каша вівсяна молочна з родзинками (200г), сир твердий (25г), чай з мелісою (200мл).',
                'lunch': 'Суп овочевий з крупою (250г), парові курячі мітболи (90г), картопляне пюре (150г), узвар (200мл).',
            }
        )

        self.stdout.write(self.style.SUCCESS('Базу даних успішно наповнено типовими зразковими даними!'))
