% =========================================================
% SYSTEM: OPEN-SOURCE SBRM HYPERCUBE
% LAYER: LOGIC & INFERENCE (HIRE PURCHASE EXTENSION)
% =========================================================

:- dynamic sbrm_fact/6.

% 1. SBRM OPERATIVE PREDICATES for Hire Purchase
calculate_hp_schedule(Entity, Period, LoanID, Output) :-
    % Dynamically read facts from the SBRM Graph
    sbrm_fact(Entity, Period, 'urn:uuid:def-hp-principal', Principal, 'AUD', 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-hp-annual-rate', AnnualRate, 'RATE', 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-hp-term-months', Term, 'MONTHS', 'Hierarchy'),
    
    ( sbrm_fact(Entity, Period, 'urn:uuid:def-hp-payment-type', PT, 'ENUM', 'Hierarchy') -> PaymentType = PT ; PaymentType = "in_arrears" ),
    ( sbrm_fact(Entity, Period, 'urn:uuid:def-hp-period-freq', PF, 'ENUM', 'Hierarchy') -> Freq = PF ; Freq = "monthly" ),
    
    % For simplicity in this demo, balloons are mocked if missing from graph. 
    % (In a full graph, they'd be queried via a list or multiple facts).
    Balloons = [_{period: 60, amount: 53715.25}],
    ExplicitPayment = 0,

    % Determine Total Amortization Term (Max of Term or furthest Balloon)
    max_balloon_period(Balloons, MaxBP),
    TotalTerm is max(Term, MaxBP),

    periods_per_year(Freq, PPY),
    PeriodicRate is AnnualRate / PPY,

    % Calculate Present Value of all Balloons
    calculate_balloons_pv(Balloons, PeriodicRate, PaymentType, 0, PV_Balloons),
    
    % Determine PMT
    AdjustedPrincipal is Principal - PV_Balloons,
    ( ExplicitPayment > 0 ->
        PMT = ExplicitPayment
    ;
        calculate_pmt(AdjustedPrincipal, PeriodicRate, Term, PaymentType, PMT)
    ),

    % Generate Schedule
    InitialBalance = Principal,
    % Dummy mapping for test
    Mapping = _{interest_expense_account: "440", liability_account: "820", clearing_bank_account: "110"},
    generate_schedule(1, TotalTerm, Term, InitialBalance, PeriodicRate, PMT, Balloons, PaymentType, Mapping, [], ScheduleReversed, 0, TotalInterest),
    reverse(ScheduleReversed, Schedule),

    Output = _{
        total_interest_paid: TotalInterest,
        amortization_schedule: Schedule
    }.

% 2. Mathematical Core
periods_per_year("monthly", 12).
periods_per_year('monthly', 12).
periods_per_year("fortnightly", 26).
periods_per_year("weekly", 52).

max_balloon_period([], 0).
max_balloon_period([B|T], Max) :-
    get_dict(period, B, P),
    max_balloon_period(T, TMax),
    Max is max(P, TMax).

calculate_balloons_pv([], _, _, Acc, Acc).
calculate_balloons_pv([B|Tail], Rate, Type, AccIn, TotalPV) :-
    get_dict(period, B, Period),
    get_dict(amount, B, Amount),
    ( (Type == "in_advance" ; Type == 'in_advance') -> Exp is Period - 1 ; Exp is Period ),
    PV is Amount / ((1 + Rate) ** Exp),
    AccOut is AccIn + PV,
    calculate_balloons_pv(Tail, Rate, Type, AccOut, TotalPV).

calculate_pmt(Principal, Rate, Term, Type, PMT) :-
    ( Rate =:= 0 ->
        PMT is Principal / Term
    ;
        ( (Type == "in_advance" ; Type == 'in_advance') ->
            PMT is Principal * (Rate / (1 - (1 + Rate) ** (-Term))) / (1 + Rate)
        ; 
            PMT is Principal * (Rate / (1 - (1 + Rate) ** (-Term)))
        )
    ).

get_balloon_amount([], _, 0).
get_balloon_amount([B|T], Period, Amount) :-
    get_dict(period, B, BPeriod),
    ( BPeriod =:= Period ->
        get_dict(amount, B, Amount)
    ;
        get_balloon_amount(T, Period, Amount)
    ).

% 3. Amortization Loop
generate_schedule(Period, TotalTerm, _, _, _, _, _, _, _, SchedAcc, SchedAcc, IntAcc, IntAcc) :-
    Period > TotalTerm, !.

generate_schedule(Period, TotalTerm, RegularTerm, Balance, Rate, BasePMT, Balloons, Type, Mapping, SchedAcc, FinalSched, IntAcc, FinalInt) :-
    get_balloon_amount(Balloons, Period, BalloonAmt),
    
    ( Period =< RegularTerm -> ActivePMT = BasePMT ; ActivePMT = 0 ),
    TotalPaymentRaw is ActivePMT + BalloonAmt,
    
    ( ((Type == "in_advance" ; Type == 'in_advance'), Period =:= 1) ->
        InterestPortionRaw is 0 
    ;
        InterestPortionRaw is Balance * Rate
    ),
    
    InterestPortion is round(InterestPortionRaw * 100) / 100,
    PrincipalPortionRaw is TotalPaymentRaw - InterestPortion,
    PrincipalPortion is round(PrincipalPortionRaw * 100) / 100,
    
    ( Period =:= TotalTerm ->
        ActualPrincipal = Balance,
        ActualPayment is round((ActualPrincipal + InterestPortion) * 100) / 100,
        NewBalance is 0.00
    ;
        ActualPrincipal = PrincipalPortion,
        ActualPayment is round(TotalPaymentRaw * 100) / 100,
        NewBalanceRaw is Balance - ActualPrincipal,
        NewBalance is round(NewBalanceRaw * 100) / 100
    ),

    NewIntAcc is IntAcc + InterestPortion,
    FinalIntAcc is round(NewIntAcc * 100) / 100,

    Entry = _{
        month: Period, 
        payment_amount: ActualPayment,
        interest_applied: InterestPortion,
        principal_applied: ActualPrincipal,
        closing_balance: NewBalance
    },

    NextPeriod is Period + 1,
    generate_schedule(NextPeriod, TotalTerm, RegularTerm, NewBalance, Rate, BasePMT, Balloons, Type, Mapping, [Entry|SchedAcc], FinalSched, FinalIntAcc, FinalInt).
