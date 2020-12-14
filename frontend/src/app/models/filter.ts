enum typefilter {
    InfGain = 'InfGain',
    CrossEntropy = 'CrossEntropy',
    MutualInfo = 'MutualInfo',
    Freq = 'Freq',
    OddsRatio = 'OddsRatio',
    NormalSeparation = 'NormalSeparation',
    Difference = 'difference',

}

export class Filter {
    typefilter: typefilter;
    sum: number;
    email: string;
    terms_freqs_positive = null;
    terms_freqs_negative = null;
}

