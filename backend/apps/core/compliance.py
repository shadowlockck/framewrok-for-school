from django.apps import apps
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta

class ComplianceAuditor:
    """
    Система аудиту інформаційної відкритості закладу освіти:
    Перевіряє повноту оприлюднення обов'язкових документів згідно зі ст. 30 ЗУ «Про освіту»,
    ст. 39 ЗУ «Про повну загальну середню освіту» та дотримання 10-денного строку оприлюднення кошторисів.
    """

    @classmethod
    def get_audit_report(cls):
        checks = []
        warnings = []

        # 1. Профіль закладу (core)
        has_core = apps.is_installed('apps.core')
        school = None
        if has_core:
            SchoolProfile = apps.get_model('core', 'SchoolProfile')
            school = SchoolProfile.objects.first()

        profile_ok = bool(school and school.name and school.edrpou and school.founder)
        checks.append({
            'code': 'profile',
            'title': 'Реквізити, ЄДРПОУ та засновник закладу',
            'law_ref': 'ст. 30 ч. 2 ЗУ «Про освіту»',
            'status': 'ok' if profile_ok else 'danger',
            'message': 'Заповнено' if profile_ok else 'Не заповнено профіль закладу або ЄДРПОУ',
            'admin_url': '/admin/core/schoolprofile/'
        })

        language_ok = bool(school and school.education_language)
        checks.append({
            'code': 'language',
            'title': 'Мова (мови) освітнього процесу',
            'law_ref': 'ст. 30 ч. 2 ЗУ «Про освіту»',
            'status': 'ok' if language_ok else 'warning',
            'message': school.education_language if language_ok else 'Не вказано мову освітнього процесу',
            'admin_url': '/admin/core/schoolprofile/'
        })

        capacity_ok = bool(school and school.licensed_capacity > 0)
        checks.append({
            'code': 'capacity_stats',
            'title': 'Ліцензований обсяг та фактична кількість осіб',
            'law_ref': 'ст. 30 ч. 2 ЗУ «Про освіту»',
            'status': 'ok' if capacity_ok else 'warning',
            'message': f"Ліцензія: {school.licensed_capacity if school else 0}, факт: {school.actual_students if school else 0}" if capacity_ok else 'Не зазначено ліцензований обсяг',
            'admin_url': '/admin/core/schoolprofile/'
        })

        # 2. Обов'язкові нормативні документи (legal)
        if apps.is_installed('apps.legal'):
            LegalDocument = apps.get_model('legal', 'LegalDocument')
            StaffMember = apps.get_model('legal', 'StaffMember')
            FinancialReport = apps.get_model('legal', 'FinancialReport')
            Vacancy = apps.get_model('legal', 'Vacancy')

            docs = LegalDocument.objects.filter(is_active=True)
            doc_titles = ' '.join(docs.values_list('title', flat=True)).lower()

            has_charter = 'статут' in doc_titles
            checks.append({
                'code': 'charter',
                'title': 'Статут закладу освіти',
                'law_ref': 'ст. 30 ч. 2 п. 1 ЗУ «Про освіту»',
                'status': 'ok' if has_charter else 'danger',
                'message': 'Оприлюднено' if has_charter else 'Статут закладу відсутній у реєстрі документів',
                'admin_url': '/admin/legal/legaldocument/'
            })

            has_license = 'ліценз' in doc_titles
            checks.append({
                'code': 'license',
                'title': 'Ліцензії на провадження освітньої діяльності',
                'law_ref': 'ст. 30 ч. 2 п. 2 ЗУ «Про освіту»',
                'status': 'ok' if has_license else 'danger',
                'message': 'Оприлюднено' if has_license else 'Ліцензію не знайдено',
                'admin_url': '/admin/legal/legaldocument/'
            })

            has_accreditation = 'акредитац' in doc_titles or 'сертифікат' in doc_titles
            checks.append({
                'code': 'accreditation',
                'title': 'Сертифікати про акредитацію освітніх програм',
                'law_ref': 'ст. 30 ч. 2 п. 3 ЗУ «Про освіту»',
                'status': 'ok' if has_accreditation else 'warning',
                'message': 'Оприлюднено' if has_accreditation else 'Сертифікати акредитації не завантажено',
                'admin_url': '/admin/legal/legaldocument/'
            })

            has_structure = 'структур' in doc_titles or 'орган' in doc_titles
            checks.append({
                'code': 'structure',
                'title': 'Структура та органи управління закладу',
                'law_ref': 'ст. 30 ч. 2 п. 4 ЗУ «Про освіту»',
                'status': 'ok' if has_structure else 'warning',
                'message': 'Оприлюднено' if has_structure else 'Документ про структуру відсутній',
                'admin_url': '/admin/legal/legaldocument/'
            })

            # Кадровий склад
            staff_count = StaffMember.objects.count()
            checks.append({
                'code': 'staff',
                'title': 'Кадровий склад згідно з ліцензійними умовами',
                'law_ref': 'ст. 30 ч. 2 п. 5 ЗУ «Про освіту»',
                'status': 'ok' if staff_count > 0 else 'danger',
                'message': f"Внесено {staff_count} працівників" if staff_count > 0 else 'Кадровий склад порожній',
                'admin_url': '/admin/legal/staffmember/'
            })

            # Річний звіт керівника
            has_annual_report = 'звіт' in doc_titles and ('керівник' in doc_titles or 'директор' in doc_titles or 'річн' in doc_titles)
            checks.append({
                'code': 'annual_report',
                'title': 'Річний звіт про діяльність закладу освіти',
                'law_ref': 'ст. 30 ч. 2 п. 12 ЗУ «Про освіту»',
                'status': 'ok' if has_annual_report else 'warning',
                'message': 'Оприлюднено' if has_annual_report else 'Публічний річний звіт керівника не знайдено',
                'admin_url': '/admin/legal/legaldocument/'
            })

            # Фінансова звітність та контроль 10 днів
            finance_reports = FinancialReport.objects.all()
            finance_count = finance_reports.count()
            overdue_reports = [r for r in finance_reports if not r.is_within_10_days]

            if overdue_reports:
                warnings.append(
                    f"Увага: {len(overdue_reports)} фінансових звітів оприлюднено з порушенням 10-денного строку з дня затвердження (ч. 3 ст. 30)!"
                )

            finance_status = 'ok'
            if finance_count == 0:
                finance_status = 'danger'
            elif overdue_reports:
                finance_status = 'warning'

            checks.append({
                'code': 'finance_reports',
                'title': 'Кошторис та фінансові звіти (строк 10 робочих днів)',
                'law_ref': 'ст. 30 ч. 3 ЗУ «Про освіту»',
                'status': finance_status,
                'message': f"Оприлюднено {finance_count} звітів (порушень строку: {len(overdue_reports)})" if finance_count > 0 else 'Жодного кошторису чи фінзвіту не оприлюднено',
                'admin_url': '/admin/legal/financialreport/'
            })

            # Конкурс на посаду керівника (ст. 39)
            director_vacancies = Vacancy.objects.filter(is_director_vacancy=True, is_open=True)
            if director_vacancies.exists():
                warnings.append(
                    "Триває конкурс на посаду керівника закладу (ст. 39 ЗУ «Про повну загальну середню освіту»). Перевірте строки подання документів!"
                )

        # 3. Зарахування та вільні місця (admissions)
        if apps.is_installed('apps.admissions'):
            ServiceTerritory = apps.get_model('admissions', 'ServiceTerritory')
            ClassCapacity = apps.get_model('admissions', 'ClassCapacity')

            territory_count = ServiceTerritory.objects.count()
            checks.append({
                'code': 'territory',
                'title': 'Закріплена територія обслуговування',
                'law_ref': 'ст. 30 ч. 2 п. 7 ЗУ «Про освіту»',
                'status': 'ok' if territory_count > 0 else 'warning',
                'message': f"Закріплено {territory_count} адрес/вулиць" if territory_count > 0 else 'Територію обслуговування не внесено',
                'admin_url': '/admin/admissions/serviceterritory/'
            })

            capacity_count = ClassCapacity.objects.count()
            checks.append({
                'code': 'class_capacity',
                'title': 'Наявність вільних місць у кожному класі',
                'law_ref': 'п. 7 Порядку зарахування учнів',
                'status': 'ok' if capacity_count > 0 else 'danger',
                'message': f"Оприлюднено для {capacity_count} класів" if capacity_count > 0 else 'Інформація про вільні місця відсутня',
                'admin_url': '/admin/admissions/classcapacity/'
            })

        # 4. Протидія булінгу (safety)
        if apps.is_installed('apps.safety'):
            AntiBullyingPolicy = apps.get_model('safety', 'AntiBullyingPolicy')
            ConfidentialReport = apps.get_model('safety', 'ConfidentialReport')

            has_policy = AntiBullyingPolicy.objects.filter(is_active=True).exists()
            unreviewed_reports = ConfidentialReport.objects.filter(is_reviewed=False).count()

            if unreviewed_reports > 0:
                warnings.append(
                    f"Нові конфіденційні звернення про булінг: {unreviewed_reports} неопрацьованих заяв потребують розгляду комісії!"
                )

            checks.append({
                'code': 'bullying_policy',
                'title': 'План заходів щодо запобігання та протидії булінгу',
                'law_ref': 'ст. 30 ч. 2 п. 14 ЗУ «Про освіту»',
                'status': 'ok' if has_policy else 'danger',
                'message': 'План та правила оприлюднено' if has_policy else 'План заходів протидії булінгу відсутній',
                'admin_url': '/admin/safety/antibullyingpolicy/'
            })

        # 5. Щоденне меню харчування (nutrition)
        if apps.is_installed('apps.nutrition'):
            DailyMenu = apps.get_model('nutrition', 'DailyMenu')
            recent_menu = DailyMenu.objects.filter(menu_date__gte=date.today() - timedelta(days=7)).exists()

            checks.append({
                'code': 'daily_menu',
                'title': 'Щоденне меню харчування та безпечність',
                'law_ref': 'Постанова КМУ № 305 / Санітарний регламент',
                'status': 'ok' if recent_menu else 'warning',
                'message': 'Оновлено на поточному тижні' if recent_menu else 'Меню на цей тиждень не завантажено',
                'admin_url': '/admin/nutrition/dailymenu/'
            })

        # Підрахунок показників
        total_count = len(checks)
        passed_count = sum(1 for c in checks if c['status'] == 'ok')
        warning_count = sum(1 for c in checks if c['status'] == 'warning')
        danger_count = sum(1 for c in checks if c['status'] == 'danger')

        score = round((passed_count / total_count) * 100) if total_count > 0 else 0

        return {
            'score': score,
            'total_count': total_count,
            'passed_count': passed_count,
            'warning_count': warning_count,
            'danger_count': danger_count,
            'warnings': warnings,
            'checks': checks,
            'is_fully_compliant': apps.is_installed('apps.legal') and score >= 90 and danger_count == 0,
        }
