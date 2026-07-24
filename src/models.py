from dataclasses import dataclass

@dataclass(frozen = True)
class SphericalFuzzyNumber:    
    #Represents a spherical fuzzy number (SFN)

    mu: float   # μ : membership degree
    nu: float   # ν : non-membership degree
    pi: float   # π : hesitancy degree

    def __post__init(self):
        if not (0 <= self.mu <= 1):
            raise ValueError(f"Invalid μ: {self.mu}")

        if not (0 <= self.nu <= 1):
            raise ValueError(f"Invalid ν: {self.nu}")

        if not (0 <= self.pi <= 1):
            raise ValueError(f"Invalid π: {self.pi}")

        if self.mu**2 + self.nu**2 + self.pi**2 > 1:
            raise ValueError(
                "Invalid Spherical Fuzzy Number: "
                f"{self.mu**2 + self.nu**2 + self.pi**2:.6f} > 1"
            )
            

    def __str__(self):
        return f"({self.mu}, {self.nu}, {self.pi})"