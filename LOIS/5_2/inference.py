# Лабораторная работа №2 по дисциплине Логические основы интеллектуальных систем
# Вариант 4: Реализовать обратный нечёткий логический вывод на основе операции нечёткой композиции 
# (min({1}v{sum({max({0}v{xi+yi-1})|i})}))
# Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А.,Германенко В.В.
# Файл, содержащий класс реализующий обратный логический вывод
from typing import Dict, List, Tuple, Optional
from decimal import Decimal, getcontext

# Настройка глобальной точности
getcontext().prec = 10

FuzzySet = List[Tuple[str, Decimal]]  
FactsDict = Dict[str, FuzzySet]
Matrix = List[List[Decimal]]
MatricesDict = Dict[str, Matrix]
# Обратный вывод: (имя_вывода, имя_множества, имя_матрицы, результирующее_множество)
ReverseInference = Tuple[str, str, str, FuzzySet]
ReverseInferenceList = List[ReverseInference]
# Границы для обратного вывода: (нижняя_граница, верхняя_граница)
Bounds = Tuple[Decimal, Decimal]
BoundsSet = List[Tuple[str, Bounds]]

class FuzzyInferenceEngine:
    """
    Класс для выполнения обратного нечёткого логического вывода
    """
    def __init__(self, facts: FactsDict, matrices: Optional[MatricesDict] = None, reverse_inferences: Optional[ReverseInferenceList] = None, eps: Decimal = Decimal('0.001')):
        # Преобразуем все значения в Decimal
        self.facts: FactsDict = {name: [(e, Decimal(str(d))) for e,d in fset] for name,fset in facts.items()}
        self.matrices: MatricesDict = matrices if matrices is not None else {}
        self.reverse_inferences: ReverseInferenceList = reverse_inferences if reverse_inferences is not None else []
        self.reverse_results:Dict[str, BoundsSet] = {}
        self.eps: Decimal = eps if isinstance(eps, Decimal) else Decimal(str(eps))
    
    def get_reverse_inferences(self):
        """Возвращает список обратных выводов"""
        return self.reverse_inferences

    def infer(self) -> FactsDict:
        """Выполняет обратный нечёткий вывод"""
        self.perform_reverse_inferences()
        return {name: [(e, d) for e,d in fset] for name,fset in self.facts.items()}
    
    def get_reverse_results(self) -> Dict[str, BoundsSet]:
        """Возвращает результаты обратных выводов"""
        return self.reverse_results


    def reverse_inference(self, matrix_name: str, output_vector: FuzzySet) -> List[BoundsSet]:
        # Подготовка данных для обратного вывода
        R, output_values, num_rows = self._prepare_reverse_inference(matrix_name, output_vector)
        if R is None:
            return []
        
        # Метод ветвей и границ: получаем набор «боксов» [L, U]
        solution_boxes = self._branch_and_bound(R, output_values, num_rows, len(output_values))
        if not solution_boxes:
            return []

        # Форматируем и объединяем результаты
        results = self._format_solution_boxes(solution_boxes, num_rows)
        merged_results = self._merge_including_solutions(results, self.eps)
        
        return merged_results
    
    def _prepare_reverse_inference(self, matrix_name: str, output_vector: FuzzySet) -> Tuple[Optional[List[List[Decimal]]], Optional[List[Decimal]], int]:
        """Подготавливает данные для обратного вывода: валидирует и преобразует в Decimal"""
        matrix = self._validate_inputs(matrix_name, output_vector)
        if matrix is None:
            return None, None, 0
        
        num_rows = len(matrix)
        num_cols = len(matrix[0]) if matrix else 0
        R, output_values = self._convert_to_decimal(matrix, output_vector, num_rows, num_cols)
        return R, output_values, num_rows
    
    def _format_solution_boxes(self, solution_boxes: List[Tuple[List[Decimal], List[Decimal]]], num_rows: int) -> List[BoundsSet]:
        """Форматирует боксы решений в список наборов границ"""
        results: List[BoundsSet] = []
        for L_vec, U_vec in solution_boxes:
            bounds = self._format_result(L_vec, U_vec, num_rows)
            results.append(bounds)
        return results
    
    def _validate_inputs(self, matrix_name: str, output_vector: FuzzySet):
        """Проверяет корректность входных данных"""
        if matrix_name not in self.matrices:
            return None
        
        matrix = self.matrices[matrix_name]
        num_rows = len(matrix)
        num_cols = len(matrix[0]) if matrix else 0
        
        if num_rows == 0 or num_cols == 0:
            return None
        
        if len(output_vector) != num_cols:
            return None
        
        return matrix
    
    def _convert_to_decimal(self, matrix: Matrix, output_vector: FuzzySet, num_rows: int, num_cols: int):
        """Преобразует матрицу и выходной вектор в Decimal"""
        R = [[Decimal(str(matrix[i][j])) for j in range(num_cols)] for i in range(num_rows)]
        output_values = [Decimal(str(deg)) for _, deg in output_vector]
        return R, output_values
    
    def _compute_forward_bounds(
        self,
        L_vec: List[Decimal],
        U_vec: List[Decimal],
        R: List[List[Decimal]],
        num_rows: int,
        num_cols: int,
    ) -> Tuple[List[Decimal], List[Decimal]]:

        B_L = [Decimal(0) for _ in range(num_cols)]
        B_U = [Decimal(0) for _ in range(num_cols)]
        
        for j in range(num_cols):
            B_L[j], B_U[j] = self._compute_bounds_for_column(L_vec, U_vec, R, num_rows, j)
        
        return B_L, B_U
    
    def _compute_bounds_for_column(
        self,
        L_vec: List[Decimal],
        U_vec: List[Decimal],
        R: List[List[Decimal]],
        num_rows: int,
        j: int,
    ) -> Tuple[Decimal, Decimal]:
        """Вычисляет нижнюю и верхнюю границы для одного столбца j"""
        sum_low = Decimal(0)
        sum_up = Decimal(0)
        for i in range(num_rows):
            sum_low += max(Decimal(0), L_vec[i] + R[i][j] - Decimal(1))
            sum_up += max(Decimal(0), U_vec[i] + R[i][j] - Decimal(1))
        B_L = min(Decimal(1), sum_low)
        B_U = min(Decimal(1), sum_up)
        return B_L, B_U
    
    def _branch_and_bound(
        self,
        R: List[List[Decimal]],
        output_values: List[Decimal],
        num_rows: int,
        num_cols: int,
    ) -> List[Tuple[List[Decimal], List[Decimal]]]:

        # Начальный гиперкуб [0,1]^n
        L0 = [Decimal(0) for _ in range(num_rows)]
        U0 = [Decimal(1) for _ in range(num_rows)]
        
        stack: List[Tuple[List[Decimal], List[Decimal]]] = [(L0, U0)]
        solutions: List[Tuple[List[Decimal], List[Decimal]]] = []
        eps = Decimal('0.01')
        max_regions = 100000
        
        iteration = 0
        while stack and len(solutions) < max_regions:
            L_vec, U_vec = stack.pop()
            iteration += 1
            
            B_L, B_U = self._compute_forward_bounds(L_vec, U_vec, R, num_rows, num_cols)
            
            # Проверка отсечения
            if self._should_prune_interval(B_L, B_U, output_values, num_cols, L_vec, U_vec, iteration):
                continue
            
            # Проверка точности
            if self._is_precise_enough(L_vec, U_vec, B_L, B_U, output_values, num_rows, num_cols, eps, iteration, solutions):
                continue
            
            # Ветвление
            L1, U1, L2, U2 = self._split_interval(L_vec, U_vec, num_rows)
            stack.append((L1, U1))
            stack.append((L2, U2))
        
        return solutions
    
    def _should_prune_interval(
        self,
        B_L: List[Decimal],
        B_U: List[Decimal],
        output_values: List[Decimal],
        num_cols: int,
        L_vec: List[Decimal],
        U_vec: List[Decimal],
        iteration: int,
    ) -> bool:
        """Проверяет, нужно ли отсечь интервал (не пересекается с целевым выходом)"""
        for j in range(num_cols):
            target = output_values[j]
            if B_U[j] < target or B_L[j] > target:
                return True
        return False
    
    def _is_precise_enough(
        self,
        L_vec: List[Decimal],
        U_vec: List[Decimal],
        B_L: List[Decimal],
        B_U: List[Decimal],
        output_values: List[Decimal],
        num_rows: int,
        num_cols: int,
        eps: Decimal,
        iteration: int,
        solutions: List[Tuple[List[Decimal], List[Decimal]]],
    ) -> bool:
        """Проверяет, достаточно ли узок интервал для добавления в решения"""
        max_width = max(U_vec[i] - L_vec[i] for i in range(num_rows))
        if max_width >= eps:
            return False
        
        # Дополнительно убеждаемся, что цель действительно лежит в [B_L, B_U]
        for j in range(num_cols):
            target = output_values[j]
            if not (B_L[j] <= target <= B_U[j]):
                return False
        
        solutions.append((L_vec, U_vec))
        return True
    
    def _split_interval(
        self,
        L_vec: List[Decimal],
        U_vec: List[Decimal],
        num_rows: int,
    ) -> Tuple[List[Decimal], List[Decimal], List[Decimal], List[Decimal]]:
        """Разделяет интервал по самой широкой координате"""
        widths = [U_vec[i] - L_vec[i] for i in range(num_rows)]
        k = max(range(num_rows), key=lambda idx: widths[idx])
        mid = (L_vec[k] + U_vec[k]) / Decimal(2)
        
        # Первый подинтервал: [L, ..., mid]
        L1 = L_vec.copy()
        U1 = U_vec.copy()
        U1[k] = mid
        
        # Второй подинтервал: [mid, ..., U]
        L2 = L_vec.copy()
        U2 = U_vec.copy()
        L2[k] = mid
        
        return L1, U1, L2, U2
    
    def _interval_includes(self, bounds1: BoundsSet, bounds2: BoundsSet, eps: Decimal) -> Optional[str]:

        if len(bounds1) != len(bounds2):
            return None
        
        bounds1_in_bounds2 = True
        bounds2_in_bounds1 = True
        
        for (elem1, (lower1, upper1)), (elem2, (lower2, upper2)) in zip(bounds1, bounds2):
            if elem1 != elem2:
                return None
            
            lower1_decimal = self._normalize_bounds_value(lower1)
            upper1_decimal = self._normalize_bounds_value(upper1)
            lower2_decimal = self._normalize_bounds_value(lower2)
            upper2_decimal = self._normalize_bounds_value(upper2)
            
            # Проверяем, включается ли [lower1, upper1] в [lower2, upper2] с погрешностью eps
            if not self._interval_included(lower1_decimal, upper1_decimal, lower2_decimal, upper2_decimal, eps):
                bounds1_in_bounds2 = False
            
            # Проверяем обратное включение
            if not self._interval_included(lower2_decimal, upper2_decimal, lower1_decimal, upper1_decimal, eps):
                bounds2_in_bounds1 = False
        
        if bounds1_in_bounds2:
            return "1_in_2"
        elif bounds2_in_bounds1:
            return "2_in_1"
        else:
            return None
    
    def _normalize_bounds_value(self, value) -> Decimal:
        """Нормализует значение границы в Decimal"""
        return value if isinstance(value, Decimal) else Decimal(str(value))
    
    def _interval_included(
        self,
        lower1: Decimal,
        upper1: Decimal,
        lower2: Decimal,
        upper2: Decimal,
        eps: Decimal,
    ) -> bool:
        return lower2 - eps <= lower1 and upper1 <= upper2 + eps
    
    
    def _merge_including_solutions(self, solutions: List[BoundsSet], eps: Decimal) -> List[BoundsSet]:

        if not solutions:
            return []
        
        merged_groups: List[BoundsSet] = []
        
        for current_bounds in solutions:
            merged_with_current = None
            merged_index = -1
            
            # Ищем, включается ли текущий интервал в какой-либо уже объединенный, или наоборот
            for idx, merged_bounds in enumerate(merged_groups):
                inclusion = self._interval_includes(current_bounds, merged_bounds, eps)
                
                if inclusion == "1_in_2":
                    # current_bounds включается в merged_bounds - объединяем с merged_bounds (больший остается)
                    merged_with_current = merged_bounds  # оставляем больший интервал
                    merged_index = idx
                    break
                elif inclusion == "2_in_1":
                    # merged_bounds включается в current_bounds - объединяем с current_bounds (больший)
                    merged_with_current = current_bounds  # используем больший интервал
                    merged_index = idx
                    break
            
            if merged_with_current is not None:
                # Объединяем с найденным интервалом (заменяем меньший на больший)
                merged_groups[merged_index] = merged_with_current
            else:
                # Добавляем как новый отдельный интервал
                merged_groups.append(current_bounds)
        
        return merged_groups
    
    def _format_result(self, lower_bounds: List[Decimal], upper_bounds: List[Decimal], num_rows: int) -> BoundsSet:
        """Формирует результат в виде списка пар (элемент, (нижняя_граница, верхняя_граница))"""
        result = []
        for i in range(num_rows):
            elem_name = f"x{i+1}"
            result.append((elem_name, (lower_bounds[i], upper_bounds[i])))
        return result

    def perform_reverse_inferences(self):
        """Выполняет все обратные логические выводы"""
        for inference_name, set_name, matrix_name, output_set in self.reverse_inferences:
            self._process_single_inference(inference_name, set_name, matrix_name, output_set)
    
    def _process_single_inference(
        self,
        inference_name: str,
        set_name: str,
        matrix_name: str,
        output_set: FuzzySet,
    ):
        """Обрабатывает один обратный вывод"""
        solutions = self.reverse_inference(matrix_name, output_set)
        
        labeled_results = []
        for idx, bounds in enumerate(solutions, start=1):
            label = f"{set_name}{idx}"
            labeled_results.append((label, bounds))
            
        self.reverse_results[inference_name] = labeled_results
    

    def _format_decimal_list(self, d_list: List[Decimal]) -> str:
        """Вспомогательная функция для форматирования списка Decimal без префикса Decimal(...)"""
        return "[" + ", ".join(f"{float(d):.6f}" for d in d_list) + "]"
