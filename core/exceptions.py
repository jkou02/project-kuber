"""Excepciones personalizadas del dominio."""


class KuberCalcException(Exception):
    """Excepción base del proyecto."""

    pass


class NotFoundError(KuberCalcException):
    """Recurso no encontrado."""

    pass


class ValidationError(KuberCalcException):
    """Error de validación de dominio."""

    pass


class DuplicateError(KuberCalcException):
    """Recurso duplicado."""

    pass
