"""
Investigation system - tracking threats and detective progress
Exact copy of This Is the President investigation mechanics
"""
import random


class Investigation:
    """An ongoing investigation into the President's crimes"""

    def __init__(self, name, investigator, severity):
        self.name = name
        self.investigator = investigator  # "FBI", "Special Counsel", "Congress"
        self.severity = severity  # 1-5, higher = more dangerous

        self.progress = 0  # 0-100, at 100 = evidence found
        self.is_active = True
        self.weeks_active = 0

        # Evidence collected
        self.evidence_strength = 0  # 0-100

    def advance(self, amount=None):
        """Investigation makes progress"""
        if not self.is_active:
            return

        if amount is None:
            # Random progress based on severity
            amount = random.randint(self.severity, self.severity * 3)

        self.progress += amount
        self.weeks_active += 1

        # Evidence accumulates
        if self.progress > 50:
            self.evidence_strength = (self.progress - 50) * 2

        if self.progress >= 100:
            self.complete()

    def setback(self, amount):
        """Investigation suffers a setback"""
        self.progress = max(0, self.progress - amount)
        self.evidence_strength = max(0, self.evidence_strength - amount // 2)

    def close(self):
        """Investigation is closed/shut down"""
        self.is_active = False
        self.progress = 0

    def complete(self):
        """Investigation completes - evidence found"""
        self.is_active = False
        return {
            'impeachment_risk': self.severity * 20,
            'evidence': self.evidence_strength
        }

    def get_danger_level(self):
        """Get current danger level"""
        if self.progress < 25:
            return "LOW"
        elif self.progress < 50:
            return "MODERATE"
        elif self.progress < 75:
            return "HIGH"
        else:
            return "CRITICAL"


class ThreatManager:
    """Manages all active threats to the presidency"""

    def __init__(self):
        self.investigations = []
        self.scandals = []
        self.witnesses = []

        # Threat levels
        self.overall_threat = 0  # 0-100

    def add_investigation(self, investigation):
        """Add new investigation"""
        self.investigations.append(investigation)
        self.update_threat_level()

    def add_scandal(self, scandal_name, severity):
        """Add new scandal"""
        self.scandals.append({
            'name': scandal_name,
            'severity': severity,
            'weeks_active': 0,
            'contained': False
        })
        self.update_threat_level()

    def add_witness(self, witness_name, knowledge):
        """Add new witness who could testify"""
        self.witnesses.append({
            'name': witness_name,
            'knowledge': knowledge,  # 0-100, how much they know
            'silenced': False,
            'cooperating': False
        })
        self.update_threat_level()

    def weekly_update(self):
        """Update all threats each week"""
        # Investigations progress
        for inv in self.investigations:
            if inv.is_active:
                inv.advance()

        # Scandals age
        for scandal in self.scandals:
            if not scandal['contained']:
                scandal['weeks_active'] += 1

        # Witnesses might flip
        for witness in self.witnesses:
            if not witness['silenced'] and random.random() < 0.1:
                witness['cooperating'] = True

        self.update_threat_level()

    def update_threat_level(self):
        """Calculate overall threat level"""
        threat = 0

        # Active investigations
        for inv in self.investigations:
            if inv.is_active:
                threat += inv.progress * inv.severity / 20

        # Active scandals
        for scandal in self.scandals:
            if not scandal['contained']:
                threat += scandal['severity'] * 5

        # Cooperating witnesses
        for witness in self.witnesses:
            if witness['cooperating'] and not witness['silenced']:
                threat += witness['knowledge'] / 5

        self.overall_threat = min(100, threat)

    def get_most_dangerous_investigation(self):
        """Get the most dangerous active investigation"""
        active = [inv for inv in self.investigations if inv.is_active]
        if not active:
            return None

        return max(active, key=lambda x: x.progress * x.severity)

    def silence_witness(self, witness_name):
        """Silence a witness (illegal)"""
        for witness in self.witnesses:
            if witness['name'] == witness_name:
                witness['silenced'] = True
                witness['cooperating'] = False
                return True
        return False

    def contain_scandal(self, scandal_name):
        """Contain/cover up a scandal"""
        for scandal in self.scandals:
            if scandal['name'] == scandal_name:
                scandal['contained'] = True
                return True
        return False


# Pre-defined investigations
INVESTIGATION_TEMPLATES = {
    'tax_fraud': Investigation(
        "Tax Fraud Investigation",
        "IRS Criminal Division",
        3
    ),

    'election_fraud': Investigation(
        "Election Interference Investigation",
        "FBI",
        4
    ),

    'obstruction': Investigation(
        "Obstruction of Justice Investigation",
        "Special Counsel",
        5
    ),

    'money_laundering': Investigation(
        "Money Laundering Investigation",
        "Treasury Department",
        4
    ),

    'foreign_collusion': Investigation(
        "Foreign Collusion Investigation",
        "Senate Intelligence Committee",
        5
    ),

    'corruption': Investigation(
        "Public Corruption Investigation",
        "FBI Public Corruption Unit",
        3
    )
}
